#ifndef LANDSCAPE_H
#define LANDSCAPE_H

#include <QHash>
#include <QVarLengthArray>
#include <QVector>
#include <QPoint>
#include <QVariant>
#include <qcolor.h>
#include <qgraphicsscene.h>
#include <QGraphicsLineItem>
#include <QGraphicsView>
#include <QApplication>
#include <QDebug>

#include <math.h>
#include <algorithm>
#include <memory>
#include "make_unique.h"

typedef QHash<QString, QVariant> Parameters;

struct Vec2 {
public:
    Vec2() : x(0), y(0) { };
    Vec2(float x, float y) : x(x), y(y) { };
    Vec2(QPointF v) : x(v.x()), y(v.y()) { };
    float x = 0;
    float y = 0;

public:
    Vec2 operator-() const { return operator*(-1); };
    void operator+=(const Vec2& other) { x += other.x; y += other.y; };
    void operator-=(const Vec2& other) { operator+=(-other); };
    Vec2 operator*(const float m) const { return Vec2{x*m, y*m}; };
    Vec2 operator/(const float m) const { return operator*(1/m); };
    Vec2 operator*(const Vec2& other) const { return Vec2{x*other.x, y*other.y}; };
    Vec2 operator+(const Vec2& other) const { return Vec2{x+other.x, y+other.y}; };
    Vec2 operator-(const Vec2& other) const { return operator+(-other); };
    float dot(const Vec2& other) const { return x*other.x + y*other.y; };
    float abs() const { return sqrt(dot(*this)); };
};

static std::default_random_engine generator;

template<int a, int b>
static int randint() {
    static std::uniform_int_distribution<int> distribution(a, b);
    return distribution(generator);
};

static int randint(int a, int b) {
    std::uniform_int_distribution<int> distribution(a, b);
    return distribution(generator);
};

static float gaussian(float a, float s) {
    std::normal_distribution<float> distribution(a, s);
    return distribution(generator);
};

static float uniform(float a, float b) {
    std::uniform_real_distribution<double> distribution(a, b);
    return distribution(generator);
};

class Branch {
private:
    Parameters params;
    Vec2 position;
    Vec2 velocity;
    int generation = 0;
    std::vector< std::unique_ptr<Branch> > branches;
    bool is_alive = true;
    bool is_dying = false;
    float gravity;
    Vec2 down_damping;
    QVector<Vec2> history;
    int branch_after;
    mutable int already_drawn = 0;

    friend class Tree;

public:
    Branch(const Vec2& position, const Vec2& velocity, Parameters params_, int generation=0)
        : params(params_)
        , position(position)
        , velocity(velocity)
        , generation(generation)
        , down_damping(params["down_damping_x"].toFloat(), params["down_damping_y"].toFloat())
    {
        history << position;
        const QPoint branch_range = params["branch_after_range"].value<QPoint>();
        branch_after = randint(branch_range.x(), branch_range.y());
        gravity = params["gravity"].toFloat();
    };

    void apply_gravity() {
        float weight = sin(atan2(velocity.x, velocity.y));
        float accel = gravity * fabs(weight);
        bool pointing_down = velocity.y < 0;
        velocity -= Vec2{0, accel} * (pointing_down ? 1 : 3);
        if ( pointing_down ) {
            velocity = velocity * down_damping;
            if ( randint(1, params["down_die_probability"].toInt()) == 4 ) {
                is_dying = true;
            }
        }
    };

    void die_if_too_old() {
        if ( history.size() > 3 && randint<8, 20>() < generation ) {
            is_alive = false;
        }
    }

    void grow() {
        for ( const std::unique_ptr<Branch>& b: branches ) {
            b->grow();
        }

        if ( position.y < randint<12, 40>() && velocity.y < 0 ) {
            is_alive = false;
        }

        die_if_too_old();

        if ( ! is_alive ) {
            return;
        }

        apply_gravity();

        position += velocity;
        history.append(position);

        if ( history.size() > branch_after ) {
            if ( params["keep_central"].toFloat() < uniform(0, 1) ) {
                is_alive = false;
            }
            if ( is_dying ) {
                return;
            }
            do_branch();
        }
    }

    void do_branch() {
        const float split = params["branch_split"].toFloat();
        const float split_var = params["branch_split_var"].toFloat();
        Vec2 v1 = velocity - Vec2{static_cast<float>(split*(1 + split_var * uniform(0.0, 1.0)-0.5)), 0};
        Vec2 v2 = velocity + Vec2{static_cast<float>(split*(1 + split_var * uniform(0.0, 1.0)-0.5)), 0};
        v1 = v1 / v1.abs() * velocity.abs() * uniform(0.9, 1.1);
        v2 = v2 / v2.abs() * velocity.abs() * uniform(0.9, 1.1);
        branches.push_back(make_unique<Branch>(position, v1, params, generation + 1));
        branches.push_back(make_unique<Branch>(position, v2, params, generation + 1));
    }

    void draw_into(QGraphicsScene* scene, bool incremental=false) const {
        for ( const std::unique_ptr<Branch>& b: branches ) {
            b->draw_into(scene, incremental);
        }
        if ( history.isEmpty() ) {
            // nothig to draw
            return;
        }

        int start = incremental ? already_drawn : 0;
        QVector<QPointF> points;
        for ( const Vec2& p: history.mid(start) ) {
            points.append(-QPointF(p.x, p.y));
        }

        float gens = params["painter_generations"].toFloat();
        float scale_factor = (params["scale"].toFloat() - 1) * 3 + 1;
        float pen_width = qMax<int>(0, gens-generation) / gens * params["painter_thickness"].toFloat() * scale_factor;

        float intensity;
        if ( generation == 0 && history.size() < 30 ) {
            intensity = 126/30.0 * history.size();
        }
        else {
            intensity = 17 + 99 * qMax<int>(0, gens-generation) / gens;
        }
        QColor color = params["color"].value<QColor>().darker(85 + (127 - intensity) * 4);
        QColor outline = color.darker(500);
        QPen pen(color);
        pen.setWidthF(pen_width);
        QPen darkPen(outline);
        darkPen.setWidthF(pen_width);
        const int depth = params["depth"].toInt();
        QPainterPath path, darkPath;
        QPointF ofs(QPointF(-1, -1) * pen_width * 0.15);
        path.moveTo(points[0]);
        darkPath.moveTo(points[0] - ofs);
        for ( int index = 1; index < points.size(); index++ ) {
            path.lineTo(points[index]);
            darkPath.lineTo(points[index] - ofs);
        }
        scene->addPath(darkPath, darkPen)->setZValue(-3);
        scene->addPath(path, pen)->setZValue(0);

        if ( incremental ) {
            already_drawn = qMax(0, history.size() - 1);
        }
    }
};

class Tree {
private:
    std::unique_ptr<Branch> trunk;

public:
    Tree(Parameters params, Vec2 base_location=Vec2(10, 0), float scale=1.0) {
        params["scale"] = scale;
        params["color"].value<QColor>().darker(1/scale * 50);
        params["depth"] = base_location.y;
        trunk = make_unique<Branch>(base_location, params["v_start"].value<QPointF>() * scale, params);
        QPoint start_range = params["start_branches"].toPoint();
        int start = randint(start_range.x(), start_range.y());
        if ( start > 1 ) {
            trunk->is_alive = false;
            trunk->generation = -1;
            for ( int i = 0; i < start / 2; i++ ) {
                trunk->do_branch();
            }
            if ( start % 2 == 1 ) {
                trunk->branches[0]->is_alive = false;
                trunk->do_branch();
            };
        }
    };

    void grow_iterations(int steps=20) {
        for ( int i = 0; i < steps; i++ ) {
            trunk->grow();
        }
    };

    void draw(QGraphicsScene* scene, bool incremental=false) {
        trunk->draw_into(scene, incremental);
    };
};

class Grass {
private:
    QGraphicsView* view;
    QRectF bounds;

public:
    Grass(QGraphicsView* forView) {
        view = forView;
        bounds = view->scene()->itemsBoundingRect();
    };

    void draw_some_grass(int bundles=100) {
        for ( int i = 0; i < bundles; i++ ) {
            float width = fabs(bounds.bottomLeft().x() - bounds.bottomRight().x());
            float x = gaussian((bounds.bottomLeft().x() + bounds.bottomRight().x()) / 2.0, width / 4.5);
            x = qMax<float>(x, bounds.bottomLeft().x() - 1.2*width);
            x = qMin<float>(x, bounds.bottomRight().x() + 1.2*width);
            float max_z = 0.35 * (bounds.topLeft().y() - bounds.bottomLeft().y());
            float z = - (pow(uniform(0, 1), 1.5) - 0.5 + uniform(-0.35, 0.35)) * max_z;
            float size = 0.25 + pow((max_z - z) / max_z, 1.5) + uniform(-0.1, 0.1);
            float y = z;
            float opacity = pow((max_z - (z+0.5*max_z)) / max_z, 2);
            draw_grass_bundle(Vec2{x, y}, size, randint(6, 14), opacity);
            if ( i % 50 == 0 ) {
                QApplication::processEvents();
            };
        }
    }

    void draw_grass_bundle(Vec2 location, float size, int items, float opacity) {
        float baseSize = 5;
        size = size * baseSize;
        float baseHeight = 0.4;
        QPen pen(QColor(180, 180, 180, opacity * 80 + 15));
        QPainterPath path;
        for ( int i = 0; i < items; i++ ) {
            int segments = 5;
            float exponent = 2.0;
            QPointF base(location.x, location.y);
            float x_diff = size * baseSize * uniform(-0.25, 0.25);
            float y_diff = size * baseSize * uniform(0.8, 1.2) * baseHeight;
            path.moveTo(base);
            for ( int segment_index = 0; segment_index < segments; segment_index++ ) {
                QPointF segment_tip(location.x + x_diff / pow(segments, exponent) * pow(segment_index + 1, exponent),
                                    location.y - y_diff / segments * segment_index);
                path.lineTo(segment_tip);
            }
        }
        view->scene()->addPath(path, pen);
    }
};

#endif
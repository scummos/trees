#include "treedialog.h"
#include <QDebug>
#include <QTime>
#include <QtOpenGL/QGLWidget>

TreeDialog::TreeDialog(QWidget* parent, Qt::WindowFlags f)
    : QDialog(parent, f)
    , ui(new Ui_Dialog)
{
    ui->setupUi(this);
    connect(ui->draw_buton, SIGNAL(clicked(bool)), SLOT(newLandscape()));
    scene = new QGraphicsScene();
    ui->image->setScene(scene);
    ui->image->setViewport(new QGLWidget(QGLFormat(QGL::SampleBuffers | QGL::DirectRendering)));
    ui->image->setRenderHints(QPainter::HighQualityAntialiasing);
    ui->image->setDragMode(QGraphicsView::ScrollHandDrag);
    ui->splitter->setSizes(QList<int>() << 100 << 500);
    connect(ui->autoRedraw, SIGNAL(clicked(bool)), SLOT(toggleAutoRedraw(bool)));
    connect(&autoTimer, SIGNAL(timeout()), SLOT(newLandscape()));
}

void TreeDialog::toggleAutoRedraw(bool checked)
{
    autoTimer.setInterval(8000);
    autoTimer.setSingleShot(false);
    if ( checked ) {
        autoTimer.start();
    }
    else {
        autoTimer.stop();
    }
}

void TreeDialog::newLandscape()
{
    int painter_id = randint(0, 1 << 31);
    active_painter = painter_id;
    int every = ui->repaint->value();

    scene->clear();

    int tree_count = ui->tree_count->value();
    int need_spacing = 65;
    QVector<Vec2> used_locations;
    for ( int tree_index = 0; tree_index < tree_count; tree_index++ ) {
        int z_range = 80;
        float base_z = uniform(-z_range, z_range);

        auto make_base = [&]() {
            return Vec2{10 + uniform(-350 + 150*tree_count, 350 + 150*tree_count), base_z};
        };
        auto closest_distance_to_used = [&](Vec2 base) {
            float closest = -1;
            for ( const Vec2& item: used_locations ) {
                float distance = abs(base.x - item.x);
                if ( closest < 0 || distance < closest ) {
                    closest = distance;
                };
            }
            return closest;
        };
        Vec2 base_location = make_base();
        while ( ! used_locations.size() == 0 && closest_distance_to_used(base_location) < need_spacing ) {
            base_location = make_base();
        }

        used_locations.append(base_location);
        float scale = 1.0 + 0.75 * pow((z_range - base_z) / (2*z_range), 2);
        Parameters params(get_params());
        Tree tree(params, base_location=base_location, scale=scale);
        for ( int iteration = 0; iteration < ui->generations->value() / every; iteration++ ) {
            QTime t;
            t.start();
            tree.grow_iterations(every);
            qDebug() << "grow:" << t.elapsed();
            t.restart();
            tree.draw(scene, true);
            qDebug() << "draw:" << t.elapsed();
            t.restart();
            ui->progress->setText(QString("Working ... displayed frame: %1").arg(iteration * every));

            QLinearGradient gradient(scene->itemsBoundingRect().topLeft(),
                                     scene->itemsBoundingRect().bottomLeft());
            gradient.setColorAt(0.4, QColor(0, 0, 0));
            gradient.setColorAt(0, QColor(25, 25, 25));
            scene->setBackgroundBrush(QBrush(gradient));

            qDebug() << "update background:" << t.elapsed();
            t.restart();
            QApplication::processEvents();
            qDebug() << "redraw:" << t.elapsed();
            if ( active_painter != painter_id ) {
                return;
            }
        }
    }

    float width = (scene->itemsBoundingRect().topLeft() - scene->itemsBoundingRect().bottomLeft()).x();
    float height = (scene->itemsBoundingRect().topLeft() - scene->itemsBoundingRect().bottomRight()).y();
    ui->image->fitInView(scene->itemsBoundingRect().adjusted(0.1*width, 0.1*height, -0.1*width, -0.1*height), Qt::KeepAspectRatio);
    Grass d(ui->image);
    d.draw_some_grass(220 + 125*tree_count);
    ui->progress->setText(QString("Done."));
}

TreeDialog::~TreeDialog()
{

}

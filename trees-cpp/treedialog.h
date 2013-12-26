#ifndef TREEDIALOG_H
#define TREEDIALOG_H

#include "ui_treedialog.h"

#include "landscape.h"

#include <QDialog>
#include <QTimer>

class TreeDialog : public QDialog {
Q_OBJECT

private:
    QGraphicsScene* scene;
    int active_painter;

public:
    explicit TreeDialog(QWidget* parent = 0, Qt::WindowFlags f = 0);
    virtual ~TreeDialog();

    Parameters get_params() {
        Parameters params;
        params["branch_split"] = ui->branch_split->value();
        params["branch_after_range"] = QPoint(ui->branch_after_min->value(), ui->branch_after_max->value());
        params["branch_split_var"] = ui->branch_split_var->value();
        params["gravity"] = ui->gravity->value();
        params["down_die_probability"] = ui->down_die_probability->value();
        params["down_damping_x"] = ui->down_damping_x->value();
        params["down_damping_y"] = ui->down_damping_x->value();
        params["start_branches"] = QPoint(ui->start_branches->value(), ui->start_branches_max->value());
        params["keep_central"] = ui->keep_central->value();
        params["color"] = QColor(ui->r->value() * 255, ui->g->value() * 255, ui->b->value() * 255);
        params["color_speed"] = ui->color_speed->value();
        params["painter_thickness"] = ui->painter_thickness->value();
        params["painter_generations"] = ui->painter_generations->value();
        QPointF start_rand(uniform(-1, 1) * ui->v_start_var->value(), uniform(-1, 1) * ui->v_start_var->value());
        params["v_start"] = QPointF(ui->v_start_x->value()+start_rand.x(), ui->v_start_y->value()+start_rand.y());
        return params;
    };

public slots:
    void newLandscape();
    void toggleAutoRedraw(bool checked);

private:
    QTimer autoTimer;
    Ui_Dialog* ui;
};

#endif
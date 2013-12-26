#include <QApplication>

#include "treedialog.h"

int main(int argc, char** argv) {
    QApplication app(argc, argv);
    TreeDialog dlg;
    dlg.show();
    dlg.newLandscape();
    app.exec();
}
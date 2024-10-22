#ifndef REGISTRATION_FORM_H
#define REGISTRATION_FORM_H

#include <QDialog>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>

namespace Ui {
class registration_form;
}

class registration_form : public QDialog
{
    Q_OBJECT

public:
    explicit registration_form(QWidget *parent = nullptr);
    ~registration_form();

private:
    Ui::registration_form *ui;
    void setup_ui();


private slots:
    void on_reg_clicked();


};
#endif // REGISTRATION_FORM_H

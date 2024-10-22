#include "registration_form.h"
#include "ui_registration_form.h"


registration_form::registration_form(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::registration_form)
{
    ui->setupUi(this);
    setup_ui();
}

void registration_form::on_reg_clicked(){
    // some actions with DB
}

void registration_form::setup_ui(){

    this->setWindowTitle("Регистрация");
    this->resize(200, 400);

    // Установка полей ввода
    ui->name_input->setPlaceholderText("Имя");
    ui->email_input->setPlaceholderText("Электронная почта");
    ui->login_input->setPlaceholderText("Логин");
    ui->password_input->setPlaceholderText("Пароль");
    ui->password_input->setEchoMode(QLineEdit::Password);
    ui->register_button->setText("Регистрация");

    // Создание и настройка вертикального компоновщика
    QVBoxLayout *layout = new QVBoxLayout();
    QLabel *welcomeLabel = new QLabel("Регистрация нового пользователя");
    QLabel *instructionLabel = new QLabel("Заполните все поля!");

    layout->addWidget(welcomeLabel);
    layout->addWidget(instructionLabel);
    layout->addWidget(ui->name_input);
    layout->addWidget(ui->email_input);
    layout->addWidget(ui->login_input);
    layout->addWidget(ui->password_input);
    layout->addWidget(ui->register_button);
    layout->setContentsMargins(50, 50, 50, 50); // Отступы от краев окна
    layout->setSpacing(20); // Расстояние между виджетами
    layout->setAlignment(Qt::AlignCenter); // Центрирование элементов

    this->setLayout(layout);

    connect(ui->register_button, &QPushButton::clicked, this, &registration_form::on_reg_clicked);
}

registration_form::~registration_form()
{
    delete ui;
}

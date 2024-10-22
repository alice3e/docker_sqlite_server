#include "login_form.h"
#include "ui_login_form.h"
#include "mainwindow.h"
#include "registration_form.h"
#include <QMessageBox>
#include <QVBoxLayout>
#include <QLabel>
#include <iostream>

login_form::login_form(QWidget *parent)
    : QDialog(parent)
    , ui(new Ui::login_form)
{
    ui->setupUi(this);
    setup_ui();  // Вызов функции настройки UI
}


void login_form::on_login_clicked()
{
    QString userlogin = ui->login_input->text().trimmed();
    QString password = ui->password_input->text().trimmed();

    if (userlogin == "admin" && password == "1234") {
        // Создаем новую страницу и показываем её
        MainWindow *main_window = new MainWindow();
        main_window->show();
        this->hide(); // Скрываем окно входа
    } else {
        // Показываем уведомление, что пароль неверный
        QMessageBox::warning(this, "Ошибка входа", "Неверное имя пользователя или пароль. Пожалуйста, попробуйте снова.");
    }
}

void login_form::on_registration_clicked()
{
    std::cout << "reg clicked";
    registration_form *reg_form = new registration_form(this);
    reg_form->exec(); // Показываем окно регистрации модально
}

void login_form::setup_ui()
{
    this->resize(400, 200);
    this->setWindowTitle("Форма входа");

    // Настройка полей ввода
    ui->login_input->setPlaceholderText("логин");
    ui->password_input->setPlaceholderText("пароль");
    ui->password_input->setEchoMode(QLineEdit::Password);

    // Создание и настройка вертикального компоновщика
    QVBoxLayout *layout = new QVBoxLayout();
    QLabel *welcomeLabel = new QLabel("Добро пожаловать в базу данных");
    QLabel *instructionLabel = new QLabel("Введите логин и пароль");
    ui->button_login->setText("Войти");
    ui->registration_button->setText("Регистрация");

    // Добавление виджетов в компоновщик
    layout->addWidget(welcomeLabel);
    layout->addWidget(instructionLabel);
    layout->addWidget(ui->login_input);
    layout->addWidget(ui->password_input);
    layout->addWidget(ui->button_login);
    //registration_button
    layout->addWidget(ui->registration_button);
    // Установка отступов и промежутков
    layout->setContentsMargins(50, 50, 50, 50); // Отступы от краев окна
    layout->setSpacing(20); // Расстояние между виджетами
    layout->setAlignment(Qt::AlignCenter); // Центрирование элементов

    // Установка компоновщика в качестве основного для формы
    this->setLayout(layout);

    // Подключение сигнала нажатия кнопки к слоту
    connect(ui->button_login, &QPushButton::clicked, this, &login_form::on_login_clicked);
    connect(ui->registration_button, &QPushButton::clicked, this, &login_form::on_registration_clicked);
}

login_form::~login_form()
{
    delete ui;
}

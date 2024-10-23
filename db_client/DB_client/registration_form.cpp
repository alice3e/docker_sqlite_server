#include "registration_form.h"
#include "ui_registration_form.h"

#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QJsonObject>
#include <QJsonDocument>
#include <QUrl>
#include <QCryptographicHash>
#include <QMessageBox>

registration_form::registration_form(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::registration_form)
{
    ui->setupUi(this);
    setup_ui();
}

void registration_form::on_reg_clicked()
{
    // Получаем значения полей из UI
    QString user_login = ui->login_input->text().trimmed();
    QString user_name = ui->name_input->text().trimmed();
    QString user_email = ui->email_input->text().trimmed();
    QString user_password = ui->password_input->text().trimmed();

    // Проверка на пустые поля
    if (user_login.isEmpty() || user_name.isEmpty() || user_email.isEmpty() || user_password.isEmpty()) {
        QMessageBox::warning(this, "Input Error", "All fields must be filled.");
        return;
    }

    // Проверка на корректность почты с использованием регулярного выражения
    QRegularExpression email_regex(R"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)");
    QRegularExpressionMatch match = email_regex.match(user_email);
    if (!match.hasMatch()) {
        QMessageBox::warning(this, "Input Error", "Invalid email address.");
        return;
    }

    // Хешируем пароль перед отправкой
    QByteArray passwordHash = QCryptographicHash::hash(user_password.toUtf8(), QCryptographicHash::Sha256);
    QString hashedPassword = passwordHash.toHex();

    // Создаем JSON-объект с данными пользователя
    QJsonObject json;
    json["name"] = user_name;
    json["email"] = user_email;
    json["login"] = user_login;
    json["password"] = hashedPassword;

    // Преобразуем JSON-объект в JSON-документ
    QJsonDocument jsonDoc(json);
    QByteArray jsonData = jsonDoc.toJson();

    // Создаем объект менеджера для выполнения запроса
    QNetworkAccessManager* manager = new QNetworkAccessManager(this);

    // Указываем URL сервера
    QUrl url("http://localhost:8000/login");
    QNetworkRequest request(url);

    // Устанавливаем заголовок, чтобы указать тип содержимого (JSON)
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    // Выполняем POST-запрос
    QNetworkReply* reply = manager->post(request, jsonData);

    // Подключаем обработчик ответа от сервера
    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            // Успешно получили ответ
            QByteArray response_data = reply->readAll();
            qDebug() << "Response from server: " << response_data;

            // Если сервер вернул успешный ответ, выводим сообщение об успехе
            QMessageBox::information(this, "Success", "Registration successful!");

        } else {
            // Ошибка при запросе
            qDebug() << "Error: " << reply->errorString();
            if(reply->errorString() == "User with this email already exists"){
                QMessageBox::warning(this, "Registration Error", "Failed to register. User with this email already exists.");
            }

            else if(reply->errorString() == "User with this login already exists"){
                QMessageBox::warning(this, "Registration Error", "Failed to register. User with this login already exists.");
            }

            else{
                QMessageBox::warning(this, "Registration Error", "Failed to register. Unknown error.");
            }

        }
        reply->deleteLater();  // Удаляем reply после обработки
    });
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

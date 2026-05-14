// author https://github.com/MIrrox27/Axion-Language

#![allow(dead_code)]
#[derive(Debug)]

pub enum AxionTokenType{
  IntegerType,  // Целое Число: 42, 100, -5
  StringType,  // Строка В Кавычках: Привет, Мир
  FloatType,  // Десятичное Число: 3.14, 2.5, 0.5
  BoolType,  // Логическое Значение: True, False
  FunctionType,  // Особый Тип Данных Для Использования В Словарях И Списках (понадобится В Будущем)
  AllType, // Специальный Тип Данных Для Использования В Словарях И Списках, Показывает Что Можно Использовать Любой Тип Данных Указанных Выше (понадобится В Будущем)


   // Ключевые Слова (зарезервированные Слова Языка)
  Fun,  // Объявление Функции: Fun(value){}
  Config,  // Объявление Конфига: Config{} (для Использования В Линуксе)
  Script,  // Объявление Начала Скрипта: Script{} (для Использования В Линуксе)
  Class,  // Объявление Класса: Class(наследование){}
  Enum,  // Объявление Перечисления: Enum{}
  Import,  // Импорт Модулей: Import Module
  Var,  // Объявление Изменяемой Переменной Var __name__  Value <- Not Const
  Val,  // Объявление Неизменяемой Переменной Val __name__  Value <- Const
  If,  // Условный Оператор: If(parameters){}
  Elif,  // Условный Оператор: Elif(parameters){}
  Else,  // Условный Оператор: Else{}
  While,  // Цикл While: While
  Do,  // Цикл Do (образован От Цикла Do While), Первый Раз Выполняется Всегда, Потом По Условию
  For,  // Цикл For: For
  Foreach,  // Цикл Foreach: Foreach(variable In Collection)
  Return,  // Возврат Значения: Return
  Is,  // Ключевое Слово Is
  In,  // Ключевое Слово In
  And,  // Ключевое Слово And (&&)
  Or,  // Ключевое Слово Or (||)
  None, // Ключевое Слово Nill (мб, Сделаем Так, Чтобы Можно Было Заменить На ;;)
  Not,  // Ключевое Слово Not, Так Же Может Обозначаться Знаком !




  Block,  // Ключевое Слово Для Обозначения Исполнения Блока Кода На Другом Языке Block __lang__{axion}
  Python,  // Ключевое Слово Для Исполнения Кода На Питоне
  CodeOpen, // Сочетание Символов Внутри Которых Находится Код На Другом Языке: {$ __code__ $}
  //code_close  Code_close // Символ Закрывающий Блок Кода: $}
  Arrow, // Символ -> (для Указания Возвращаемых Переменных)


    // Операторы (математические И Логические Операции)
  Plus,  // Сложение: +
  Minus,  // Вычитание: -
  Increment,  // ++x
  Decrement,  // --x
  PostIncrement,  // X++
  PostDecrement,  // X--
  Multiply,  // Умножение: *
  Divide,  // Деление: /
  Assign,  // Присваивание: 
  Equals,  // Равенство: 
  NotEquals,  // Неравенство: !
  Less,  // Меньше: <
  Greater,  // Больше: >
  Mod,  // %
  Power, // Степень Числа: **
  LessEqual,  // <
  GreaterEqual, // >


      // Разделители (пунктуация И Скобки)
  LParen,  // Левая Круглая Скобка: (
  RParen,  // Правая Круглая Скобка: )
  LBrace,  // Левая Фигурная Скобка: {
  RBrace,  // Правая Фигурная Скобка: }
  LBracket, // Левая Квадратная Скобка: [
  RBracket,  // Правая Квадратная Скобка: ]
  Semicolon,  // Точка С Запятой: ;
  Colon,  // Двоеточие: :
  Comma,  // Запятая: ,
  Dot,  // Точка .


  // Специальные Токены
  Eof,  // Конец Файла (end Of File)
  Identifier,  // Идентификатор (имя Переменной/функции)


  Axion,  // Проверочный Токен Для Языка Axion
}






#[derive(Debug)]
pub struct AxionToken {
    pub token_type: AxionTokenType,
    pub value: Option<String>,
    pub line: usize

} 

impl AxionToken {
    pub fn new(token_type: AxionTokenType, value: Option<String>, line: usize) -> Self{
      AxionToken { token_type, value, line }
    }
}

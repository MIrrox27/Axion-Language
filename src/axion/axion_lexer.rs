// author https://github.com/MIrrox27/Axion-Language

//use std::hint::select_unpredictable;

use super::axion_tokens::AxionToken; 
use super::axion_tokens::AxionTokenType; 
use std::collections::HashMap;
use phf::phf_map;



static KEYWORDS: phf::Map<&'static str, AxionTokenType> = phf_map! {
  "import"  => AxionTokenType::Import,

  "if" => AxionTokenType::If,
  "elif" => AxionTokenType::Elif,
  "else" => AxionTokenType::Else,

  "while" => AxionTokenType::While,
  "do" => AxionTokenType::Do,
  "for" => AxionTokenType::For,
  "foreach" => AxionTokenType::Foreach,

  "var"  => AxionTokenType::Var,
  "val"  => AxionTokenType::Val,

  "True"  => AxionTokenType::BoolType,
  "False"  => AxionTokenType::BoolType,

  "class"  => AxionTokenType::Class,
  "enum" => AxionTokenType::Enum,

  //"script" => AxionTokenType::SCRIPT,
  //"config" => AxionTokenType::CONFIG,

  "block" => AxionTokenType::Block,
  "python" => AxionTokenType::Python,

  "is" => AxionTokenType::Is,
  "in" => AxionTokenType::In,
  "and" => AxionTokenType::And,
  "or" => AxionTokenType::Or,
  "None" => AxionTokenType::NoneType,
  "not" => AxionTokenType::Not,
};


  
pub struct AxionLexer{
  text: Vec<char>,
  position: usize,
  line: usize,
  //current_char: Option<char>
  end: bool
}


impl AxionLexer { // Системные (вспомогательные) функции

  fn error(&mut self, msg: &str, func: &str){
    panic!("[ERROR] [AxionLexer] ({}): {}", func, msg)
  }
    
}

impl AxionLexer {

    fn current_char(&self) -> Option<char>{ // Вместо переменной, будет каждый раз нахожиться сл символ
      self.text.get(self.position).copied()
    }
    

    fn current_is_withspace(&self) -> bool{
      match self.current_char() {
        Some(ch) => ch.is_whitespace(),
        None => false
      }
    }

    
    fn new(code: String) -> Self {
      let chars: Vec<char> = code.chars().collect();
      let pos: usize = 0;
      let line: usize = 1;

      AxionLexer { text: chars, position: pos, line: line, end: false }
    }

    fn adwance(&mut self){
      let newline: char = '\n';

      if self.current_char() == Some(newline) {
        self.line += 1;
      }
      self.position += 1;

      if self.position >= self.text.len(){
          self.end = true;
      }      
    }

    fn retrat(&mut self){
      self.position -= 1;

      if self.position >= self.text.len(){
          self.end = true;
      }      
    }


    fn peek_position(&mut self, lookhead: usize) -> Option<char>{
      let peek_position = self.position + lookhead;

      if peek_position >= self.text.len(){
        return None;
      }

      return self.text.get(peek_position).copied();
    }




    fn skip_withspace(&mut self){
      let newline: char = '\n';

      while self.current_char() != None || self.current_is_withspace() {
        
        if self.current_char() == Some(newline) {
            self.line += 1;
        }
          self.adwance();
      }
    }


    fn skip_comment(&mut self) {
      let newline: char = '\n';
      while self.current_char() != None || self.current_char() != Some(newline){
        self.adwance();
      }
      if self.current_char() == Some(newline){
        self.adwance();
      }
    }


    fn read_code_block(){} // Пока не реализуем 


    fn read_string_single_quotes(&mut self){
      let quot: Option<char> = Some('\'');

      self.adwance(); // Пропускаем первую кавычку
      let mut result: String = String::new();
      
      while self.current_char() != None || self.current_char() != quot{
          let current_char_str: String = self.current_char().map(|c| c.to_string()).unwrap_or_default();
          result = format!("{}{}", result, current_char_str);
          self.adwance();
      }

      if self.current_char() != quot{
        self.error("Second quotation mark not found", "read_string_single_quotes");
      }

    }


    fn read_string_double_quotes(&mut self){
      let quot: Option<char> = Some('"');

      self.adwance(); // Пропускаем первую кавычку
      let mut result: String = String::new();
      
      while self.current_char() != None || self.current_char() != quot{
          let current_char_str: String = self.current_char().map(|c| c.to_string()).unwrap_or_default();
          result = format!("{}{}", result, current_char_str);
          self.adwance();
      }

      if self.current_char() != quot{
        self.error("Second quotation mark not found", "read_string_single_quotes");
      }




    }




}

    



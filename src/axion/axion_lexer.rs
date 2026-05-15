// author https://github.com/MIrrox27/Axion-Language

use super::axion_tokens::AxionToken; 
use super::axion_tokens::AxionTokenType; 

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

impl AxionLexer {

    fn current_char(&self) -> Option<char>{ // Вместо переменной, будет каждый раз нахожиться сл символ
      self.text.get(self.position).copied()
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


}

    



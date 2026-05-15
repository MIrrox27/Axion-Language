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


  
pub struct AxionLexer{}
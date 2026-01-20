const Joi = require('joi');

exports.create = Joi.object({
  nome: Joi.string()
    .required()
    .min(3)
    .max(100)
    .messages({
      'string.base': 'Nome deve ser um texto',
      'string.empty': 'Nome não pode estar vazio',
      'string.min': 'Nome deve ter no mínimo 3 caracteres',
      'string.max': 'Nome não pode ter mais de 100 caracteres',
      'any.required': 'Nome é obrigatório'
    }),
  crm: Joi.string()
    .required()
    .min(4)
    .max(20)
    .messages({
      'string.base': 'CRM deve ser um texto',
      'string.empty': 'CRM não pode estar vazio',
      'string.min': 'CRM deve ter no mínimo 4 caracteres',
      'string.max': 'CRM não pode ter mais de 20 caracteres',
      'any.required': 'CRM é obrigatório'
    }),
  especialidade: Joi.string()
    .required()
    .min(3)
    .max(50)
    .messages({
      'string.base': 'Especialidade deve ser um texto',
      'string.empty': 'Especialidade não pode estar vazia',
      'string.min': 'Especialidade deve ter no mínimo 3 caracteres',
      'string.max': 'Especialidade não pode ter mais de 50 caracteres',
      'any.required': 'Especialidade é obrigatória'
    })
});

exports.update = Joi.object({
  nome: Joi.string()
    .min(3)
    .max(100)
    .messages({
      'string.base': 'Nome deve ser um texto',
      'string.empty': 'Nome não pode estar vazio',
      'string.min': 'Nome deve ter no mínimo 3 caracteres',
      'string.max': 'Nome não pode ter mais de 100 caracteres'
    }),
  crm: Joi.string()
    .min(4)
    .max(20)
    .messages({
      'string.base': 'CRM deve ser um texto',
      'string.empty': 'CRM não pode estar vazio',
      'string.min': 'CRM deve ter no mínimo 4 caracteres',
      'string.max': 'CRM não pode ter mais de 20 caracteres'
    }),
  especialidade: Joi.string()
    .min(3)
    .max(50)
    .messages({
      'string.base': 'Especialidade deve ser um texto',
      'string.empty': 'Especialidade não pode estar vazia',
      'string.min': 'Especialidade deve ter no mínimo 3 caracteres',
      'string.max': 'Especialidade não pode ter mais de 50 caracteres'
    })
}).min(1).messages({
  'object.min': 'Pelo menos um campo deve ser fornecido para atualização'
});

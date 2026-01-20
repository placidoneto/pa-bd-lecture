const Joi = require('joi');

exports.create = Joi.object({
  medicoId: Joi.number()
    .integer()
    .required()
    .messages({
      'number.base': 'ID do médico deve ser um número',
      'number.integer': 'ID do médico deve ser um número inteiro',
      'any.required': 'ID do médico é obrigatório'
    }),
  data: Joi.date()
    .iso()
    .required()
    .messages({
      'date.base': 'Data deve ser uma data válida',
      'date.format': 'Data deve estar no formato ISO (YYYY-MM-DD)',
      'any.required': 'Data é obrigatória'
    }),
  horarioInicio: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .required()
    .messages({
      'string.base': 'Horário de início deve ser um texto',
      'string.pattern.base': 'Horário de início deve estar no formato HH:mm',
      'any.required': 'Horário de início é obrigatório'
    }),
  horarioFim: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .required()
    .messages({
      'string.base': 'Horário de fim deve ser um texto',
      'string.pattern.base': 'Horário de fim deve estar no formato HH:mm',
      'any.required': 'Horário de fim é obrigatório'
    }),
  local: Joi.string()
    .required()
    .min(3)
    .max(100)
    .messages({
      'string.base': 'Local deve ser um texto',
      'string.empty': 'Local não pode estar vazio',
      'string.min': 'Local deve ter no mínimo 3 caracteres',
      'string.max': 'Local não pode ter mais de 100 caracteres',
      'any.required': 'Local é obrigatório'
    })
});

exports.update = Joi.object({
  medicoId: Joi.number()
    .integer()
    .messages({
      'number.base': 'ID do médico deve ser um número',
      'number.integer': 'ID do médico deve ser um número inteiro'
    }),
  data: Joi.date()
    .iso()
    .messages({
      'date.base': 'Data deve ser uma data válida',
      'date.format': 'Data deve estar no formato ISO (YYYY-MM-DD)'
    }),
  horarioInicio: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .messages({
      'string.base': 'Horário de início deve ser um texto',
      'string.pattern.base': 'Horário de início deve estar no formato HH:mm'
    }),
  horarioFim: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .messages({
      'string.base': 'Horário de fim deve ser um texto',
      'string.pattern.base': 'Horário de fim deve estar no formato HH:mm'
    }),
  local: Joi.string()
    .min(3)
    .max(100)
    .messages({
      'string.base': 'Local deve ser um texto',
      'string.empty': 'Local não pode estar vazio',
      'string.min': 'Local deve ter no mínimo 3 caracteres',
      'string.max': 'Local não pode ter mais de 100 caracteres'
    })
}).min(1).messages({
  'object.min': 'Pelo menos um campo deve ser fornecido para atualização'
});

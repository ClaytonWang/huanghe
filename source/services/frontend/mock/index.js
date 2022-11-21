/**
 * @description Mock代理
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const { genProxy } = require('./utils');
const _proxy = {
  // 'FORM /api/v1/ladder/agents/upload': (req, res) => {
  //   return res.json({
  //     success: true,
  //     message: '',
  //   })
  // },
  // 'FORM /api/v1/ladder/policies/upload': (req, res) => {
  //   return res.json({
  //     success: true,
  //     message: '',
  //   })
  // },
};
const proxy = Object.assign(genProxy(), _proxy);
module.exports = proxy;

/**
 * @description mock工具方法
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
/* eslint-disable @typescript-eslint/no-var-requires */
const { get, assign } = require('lodash');
const {
  apiPrefix,
  api,
  apiUriParamsPattern,
} = require('../src/common/utils/config');
const success = {
  success: true,
  message: '',
  status: 200,
  result: {},
};
const ok = (data) => assign({}, success, { result: data });
const error = () => ({
  success: false,
  message: '',
  status: 400,
});
const list = (req, res, obj) => {
  let requestParams = assign({}, req.query, req.body);
  let pageParams = {
    pageno: requestParams.pageno ? parseInt(requestParams.pageno, 10) : 1,
    pagesize: requestParams.pagesize
      ? parseInt(requestParams.pagesize, 10)
      : 30,
    total: (obj.result || obj.data || []).length ? 100 : 0,
    order: requestParams.order,
    orderBy: requestParams.orderBy,
  };
  let result = assign(pageParams, obj);
  end(res, { result });
};
const end = (res, data) => {
  setTimeout(() => {
    res.end(JSON.stringify(assign({}, success, data)));
  }, 800);
};
// 代理生成器
const genProxy = () => {
  const proxy = {};
  Object.values(api).forEach((value) => {
    const method = value.split('|')[0].toUpperCase();
    const path = value.split('|')[1];
    const url = apiPrefix + path;
    proxy[`${method} ${url}`] = (req, res) => {
      let suffix = '';
      if (method === 'GET' && get(req, 'query.type')) {
        suffix = `/${get(req, 'query.type')}`;
      }
      const filePath = path.replace(
        apiUriParamsPattern,
        (_match, field) => field
      );
      const result = require(`.${filePath}${suffix}/${method}.js`);
      if (typeof result === 'function') {
        return result(req, res);
      }
      return res.json(result);
    };
  });
  return proxy;
};

module.exports = {
  genProxy,
  ok,
  error,
  list,
};

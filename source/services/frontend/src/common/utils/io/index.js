/**
 * @description 请求发送器
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { message, Modal } from 'antd';
import axios from 'axios';
import { isString, isEmpty, cloneDeep } from 'lodash';
import qs from 'qs';
import { apiPrefix } from '@/common/utils/config';
import { history } from '@/app/history';
import {
  parseKeyToCamel,
  parseKeyToSnake,
  parseUrl,
  tranverseJson,
} from '../helper';

const codeMessage = {
  200: '服务器成功返回请求的数据',
  201: '新建或修改数据成功。',
  202: '一个请求已经进入后台排队（异步任务）',
  204: '删除数据成功。',
  400: '发出的请求有错误，服务器没有进行新建或修改数据的操作。',
  401: '用户名或者密码错误。',
  403: '用户得到授权，但是访问是被禁止的。',
  404: '发出的请求针对的是不存在的记录，服务器没有进行操作',
  406: '请求的格式不可得。',
  410: '请求的资源被永久删除，且不会再得到的。',
  422: '当创建一个对象时，发生一个验证错误。',
  500: '服务器发生错误，请检查服务器',
  502: '网关错误',
  503: '服务不可用，服务器暂时过载或维护',
  504: '网关超时',
};

/**
 * 生成全局错误对象
 *
 * @param {string} message 错误提示信息
 * @return {Object} 全局错误对象
 */
function getGlobalError(msg) {
  return {
    success: false,
    message: msg,
  };
}

const NETWORK_ERROR = getGlobalError('网络错误');

/**
 * 处理服务端响应成功的情况
 *
 * @param {meta.Promise} response 响应的Promise
 * @return {meta.Promise} 处理后的Promise
 */
function requestSuccessHandler(response) {
  if (response.success === false) {
    const { message: _msg } = response;
    if (_msg) {
      message.error(_msg);
    }
    return Promise.reject(_msg);
  }
  return Promise.resolve(response);
}

/**
 * 处理服务端响应失败的情况
 * 转换为成功响应，返回错误提示处理
 *
 * @param {meta.Promise} error 响应的Promise
 * @return {meta.Promise} 处理后的Promise
 */
function requestFailureHandler(error) {
  const { response } = error;
  let errorType;
  if (response) {
    const { status: _status } = response;
    // 服务器没有正常返回
    if (_status < 200 || (_status >= 400 && _status !== 401 && _status < 500)) {
      errorType =
        (!(response.data instanceof Blob) && response.data) ||
        getGlobalError(codeMessage[_status]);
    } else if (_status === 401) {
      Modal.warning({
        title: '系统提示',
        content: '用户登录失效，请重新登录！',
      });
      // clear localstorage token
      window.localStorage.clear();
      history.push('/login');
      return Promise.reject(codeMessage[_status]);
    } else if (error.message) {
      errorType = getGlobalError(error.message);
    } else {
      errorType = NETWORK_ERROR;
    }
  } else if (error.message) {
    errorType = getGlobalError(error.message);
  } else {
    errorType = NETWORK_ERROR;
  }
  return requestSuccessHandler(errorType);
}

export class IO {
  axios = axios.create({
    responseType: 'json',
  });

  apis = {};

  hooks = {};

  me = null;

  /* eslint no-param-reassign: ["error", { "props": false }] */
  constructor() {
    this.axios.interceptors.request.use((config) => {
      const token = JSON.parse(window.localStorage.getItem('token'));
      // 请求时，headers中添加token
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
    this.axios.interceptors.response.use((response) => {
      // IE9 不支持 responseType 配置，所以 response.data 始终都不会存在，
      // 手动从 response.request.responseText 中 parse。
      let data = cloneDeep(
        response.data || JSON.parse(response.request.responseText)
      );
      data = tranverseJson(data, parseKeyToCamel);
      return requestSuccessHandler.call(this, data);
    }, requestFailureHandler.bind(this));
  }

  request(...args) {
    return this.axios(...args);
  }
  get(...args) {
    return this.axios.get(...args);
  }
  post(url, data, configs) {
    // 兼容指定content-type为form的格式
    if (
      configs &&
      configs.headers &&
      configs.headers['Content-Type'] === 'application/x-www-form-urlencoded'
    ) {
      return this.axios.post(url, qs.stringify(data), configs);
    }
    return this.axios.post(url, data, configs);
  }
  patch(url, data, configs) {
    return this.axios.patch(url, data, configs);
  }
  put(url, data, configs) {
    return this.axios.put(url, data, configs);
  }
  delete(url, data, configs) {
    return this.axios.delete(url, data, configs);
  }
  // 封装请求发送器
  create(key, url) {
    const genRequester = (_url) => {
      let url = _url;
      if (isString(url)) {
        // 只有一个URL，直接返回封装过的请求方法
        let urlInfo = url.split('|');
        let method = urlInfo.length > 1 ? urlInfo[0] : 'get';
        url = apiPrefix + (urlInfo[1] || urlInfo[0]);
        // 过滤掉不需要生成的URL
        const isRequester = (path) =>
          // 默认跳过以`/download`和`/upload`结尾的路径
          !/\/(?:up)load$/.test(path);
        return (data = {}, configs = {}) => {
          let uri = url;
          // 不需要生成请求函数的，将参数拼接到URL上
          if (!isRequester(uri)) {
            if (!isEmpty(data)) {
              return `${uri}?${qs.stringify(data)}`;
            }
            return uri;
          }
          let _data = cloneDeep(data);
          _data = tranverseJson(_data, parseKeyToSnake);
          uri = parseUrl(uri, _data);
          if (method === 'get') {
            return this.get(uri, {
              params: _data,
              paramsSerializer(params) {
                return qs.stringify(params, { arrayFormat: 'comma' });
              },
              ...configs,
            });
          }
          return this[method](uri, _data, configs);
        };
      }
    };
    this.apis[key] = genRequester(url);
  }
  getApis() {
    return { ...this.apis };
  }
}

export default new IO();

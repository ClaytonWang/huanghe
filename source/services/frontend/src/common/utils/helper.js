/**
 * @description common functions
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import React from 'react';
import { uniqueId, cloneDeep, debounce } from 'lodash';
import accounting from 'accounting';
import moment from 'moment';
import { apiUriParamsPattern } from '@/common/utils/config';
/**
 * parse router as xxx/:xx to url
 * @param {string} _url
 * @param {object} params
 * @param {object} data
 * @return {url}
 */
export const parseUrl = (_url, params) => {
  // if url router as xxx/:xx_xxx, replace params
  const url = _url.replace(apiUriParamsPattern, (_match, field) => {
    if (field in params) {
      const value = params[field];
      // remove matched value from params
      delete params[field];
      return value;
    }
    throw new Error(
      `Cannot found params "${field}" to repalce url pattern "pattern"`
    );
  });
  return url;
};

/**
 * transfer array to map
 * @param {array} arr
 * @return {object}
 */
export const arrayToMap = (arr) => {
  let map = {};
  for (let i = 0; i < arr.length; i += 1) {
    if (arr[i] instanceof Object) {
      map = { ...map, ...arr[i] };
    } else {
      map[i] = arr[i];
    }
  }
  return map;
};

/**
 * transfer function to promise
 * @param {function} fn
 * @return {promise}
 */
export const promisify = (fn) => (args, data, callback) =>
  new Promise((resolve) => {
    if (typeof callback === 'function') {
      fn(args, () => {
        resolve(callback(data));
      });
    } else {
      fn(args, () => {
        resolve(data);
      });
    }
  });

/**
 * 根据前缀生成唯一的 key
 *
 * @param {string} prefix 前缀
 * @return {string} 返回唯一的 key
 */
export function genRowKey(prefix) {
  return uniqueId(`${prefix}_`);
}

/**
 * 使用accounting转成通用数值展示
 *
 * @param {number} value 数值
 * @return {string}
 */
export const formatNumber = (value) => accounting.format(value, 2);

/**
 * 转换KV到key, value格式
 *
 * @param {object} obj
 * @param {string} key key字段名
 * @param {string} value value字段名
 * @return {array} [{key: value}]
 */
export const parseKVToKeyValue = (obj, key, value) =>
  Object.keys(obj).map((k) => ({
    [key]: k,
    [value]: obj[k],
  })) || [];
/**
 * 转换key, value到KV格式
 *
 * @param {array} obj
 * @return {object} {k: v, k2: v2}
 */
export const parseKeyValueToKV = (arr) => {
  let obj = {};
  arr.forEach(([key, value]) => Object.assign(obj, { [key]: value }));
  return obj;
};
/**
 * 将时间数据转换为 YYYY/MM/DD HH:mm:ss 格式字符串输出
 *
 * @param {number|string} value
 * @return {string} YYYY/MM/DD HH:mm:ss
 */
export const transformTime = (value, format = 'YYYY/MM/DD HH:mm:ss') => {
  if (!value) {
    return '';
  }
  return moment(value).format(format);
};

/**
 * 将日期时间转换为 YYYY-MM-DD 格式字符串输出
 *
 * @param {number|string} value
 * @return {string} YYYY-MM-DD
 */
export const transformDate = (value, format = 'YYYY-MM-DD') => {
  if (!value) {
    return '';
  }
  return moment(value).format(format);
};
/**
 * promise顺序执行task
 *
 * @param {array} tasks
 * @return
 */
export const sequencePromise = (tasks) => {
  tasks.reduce(
    (promise, task) => promise.then((value) => task(value)),
    Promise.resolve()
  );
};
/**
 * 遍历树形结构，执行回调
 *
 * @param {array|object} tree
 * @param {function} fn 处理函数，参数是item
 * @return
 */
export const tranverseTree = (tree, fn, param = []) => {
  if (tree instanceof Array) {
    for (let item of tree) {
      if (item.children) {
        tranverseTree(item.children, fn, param);
      }
      fn(item, ...param);
    }
  }
  // 根节点为对象
  else if (tree instanceof Object) {
    let node = tree;
    if (tree.children && tree.children.length) {
      tranverseTree(node, fn, param);
    }
    fn(node, ...param);
  }
  return;
};
/**
 * 遍历树形结构，返回新的树
 *
 * @param {array} tree
 * @param {array} arr 结果集合
 * @param {function} exec 处理函数
 * @param {function} param 处理函数其他参数
 * @return 新的树结构
 */
export const tranverseTree2 = (tree = [], arr = [], exec, param = []) => {
  if (!tree.length) return [];
  for (let item of tree) {
    let node = { ...item, children: [] };
    if (exec) {
      node = exec(item, ...param);
    }
    arr.push(node);
    if (item.children && item.children.length) {
      tranverseTree2(item.children, (node.children = []), exec, param);
    }
  }
  return arr;
};
/**
 * 过滤树形结构，返回符合条件的树结构
 *
 * @param {array} tree
 * @param {function} validator
 * @param {array} param 校验函数参数
 * @param {array} arr 中间结果
 * @param {array} arr 过滤结果
 * @return
 */
export const filterTree = (
  tree = [],
  validator = () => {},
  param = [],
  arr = []
) => {
  if (!tree.length) return [];
  for (let item of tree) {
    if (!validator([item, ...param])) continue;
    let node = { ...item, children: [] };
    arr.push(node);
    if (item.children && item.children.length) {
      filterTree(item.children, validator, param, node.children);
    }
  }
  return arr;
};
/**
 * 判断当前节点是否为叶子结点
 *
 * @param {object} item
 * @return boolean
 */
export const isLeafNode = (item) => !(item && item.children);

/**
 * 将数组转成指定key的map
 *
 * @param {array} arr
 * @param {string} key
 * @return [{ [key]: value }]
 */
export const arrayToMapByKey = (arr, key) =>
  arr.map((value) => ({ [key]: value }));

/**
 * 深度查找，去掉对象中的空字段
 *
 * @param {object} obj
 * @return object
 */
export const purifyDeep = (obj) => {
  const result = cloneDeep(obj);
  Object.keys(result).forEach((k) => {
    if (result[k] instanceof Object) {
      result[k] = purifyDeep(result[k]);
    }
    if (!result[k] || result[k] === 'all') {
      delete result[k];
    }
  });
  return result;
};
/**
 * 蛇形表达式
 *
 * @param {string} value
 * @return boolen
 */
export const isSnakecase = (value) => {
  console.log();
  return /\w+_\w+/.test(value);
};
/**
 * 蛇形转驼峰
 *
 * @param {string} value
 * @return string
 */
export const parseSnakeToCamel = (value) => {
  console.log();
  const pattern = /_([a-z])/;
  return value.replace(pattern, (_all, letter) => letter.toUpperCase());
};
/**
 * 驼峰表达式
 *
 * @param {string} value
 * @return boolen
 */
export const isCamelcase = (value) => {
  console.log();
  return /[a-z]+([A-Z])[a-z]+/.test(value);
};
/**
 * 驼峰转蛇形
 *
 * @param {string} value
 * @return string
 */
export const parseCamelToSnake = (value) => {
  console.log();
  const pattern = /([a-z])([A-Z])/;
  return value.replace(pattern, (_all, sub1, sub2) => {
    console.log();
    return `${sub1}_${sub2.toLowerCase()}`;
  });
};
/**
 * 遍历Json对象
 *
 * @param {string} value
 * @return string
 */
export const tranverseJson = (json, fn) => {
  if (json instanceof Array) {
    let arr = json;
    for (let item of arr) {
      if (item) {
        item = tranverseJson(item, fn);
      }
    }
    return arr;
  }
  // 根节点为对象
  if (json instanceof Object) {
    let obj = json;
    Object.entries(obj).forEach(([key, value]) => {
      if (value instanceof Object) {
        obj[key] = tranverseJson(value, fn);
      }
      fn(obj, [key, value]);
    });
    return obj;
  }
  return json;
};
/**
 * 遍历Json对象
 *
 * @param {string} value
 * @return string
 */
export const parseKeyToCamel = (obj, [key, value]) => {
  if (isSnakecase(key)) {
    let newKey = key;
    delete obj[key];
    newKey = parseSnakeToCamel(key);
    obj[newKey] = value;
  }
};
/**
 * 遍历Json对象
 *
 * @param {string} value
 * @return string
 */
export const parseKeyToSnake = (obj, [key, value]) => {
  if (isCamelcase(key)) {
    let newKey = key;
    delete obj[key];
    newKey = parseCamelToSnake(key);
    obj[newKey] = value;
  }
};
/**
 * 给定两个日期，返回相对日期。
 *
 * @param {Date} from
 * @param {Date} to
 * @return number
 */
export const relativeDate = (start, end) => moment(start).diff(end, 'days');
/**
 * 给定前缀，返回该前缀唯一Id
 *
 * @param {String} prefix
 * @return string
 */
const Counter = function () {
  let counter = 0;
  this.getCounter = function () {
    counter = counter + 1;
    return counter;
  };
};
export const ID = function () {
  let obj = {};
  this.getValue = function (prefix) {
    if (!obj[prefix]) {
      obj[prefix] = new Counter();
    }
    return `${prefix}${obj[prefix].getCounter()}`;
  };
};
const globalID = new ID();
export const genUniqueIdByPrefix = (prefix, instance) => {
  if (!prefix) {
    throw new Error('need a prefix');
  }
  if (instance) {
    return instance.getValue(prefix);
  }
  return globalID.getValue(prefix);
};

export const pageSetToRoutes = (pages) => {
  const pageProcessor = ([name, page]) => {
    const route = {
      path: page.path ?? '',
    };

    route.exact = !!page.exact;
    route.modal = !!page.modal;

    if (page.title) route.title = page.title;
    if (page.render) route.render = page.render;

    if (page instanceof React.Component || page instanceof Function) {
      if (name && /Layout/.test(name)) route.layout = page;
      else route.component = page;
    } else {
      route.component = page.component;
      route.layout = page.layout;
    }

    if (route.component?.context) route.context = route.component.context;

    return route;
  };

  try {
    if (Array.isArray(pages)) {
      return pages.map((page) => pageProcessor([null, page]));
    }
    return Object.entries(pages).map(pageProcessor);
  } catch (err) {
    console.log(err);
    return [];
  }
};

export const getStatusName = (value) => {
  let status = value;
  // eslint-disable-next-line default-case
  switch (status) {
    case 'stop_fail':
    case 'run_fail':
    case 'start_fail':
      status = 'error';
      break;
    case 'run':
      status = 'running';
      break;
  }
  return status;
};
/**
 * 给事件增加防抖
 *
 * @param {function} event
 * @param {number} duration
 * @return function
 */
export const debounceEvent = (event, duration = 1000) =>
  debounce(event, duration, {
    leading: true,
    trailing: false,
  });
/**
 * 拼接对象数组
 *
 * @param {array} arr
 * @param {string} splitter
 * @param {function} getValue
 * @return string
 */
export const join = (arr, splitter = ',', getValue) => {
  if (!arr || arr.length <= 0) return '';
  return arr.reduce((prev, curr) => {
    if (prev) {
      if (getValue) {
        return `${prev}${splitter}${getValue(curr)}`;
      }
      return `${prev}${splitter}${curr}`;
    }
    return getValue && `${getValue(curr)}`;
  }, null);
};

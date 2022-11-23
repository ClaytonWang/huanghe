/**
 * @description common functions
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */

import { uniqueId, cloneDeep } from 'lodash';
import accounting from 'accounting';
import moment from 'moment';
/**
 * parse router as xxx/:xx to url
 * @param {string} _url
 * @param {object} params
 * @param {object} data
 * @return {url}
 */
export const parseUrl = (_url, params) => {
  // if url router as xxx/:xx, replace params
  const url = _url.replace(/:([a-zA-Z0-9]+)/g, (_match, field) => {
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
 * @param {number} value
 * @return {string} YYYY/MM/DD HH:mm:ss
 */
export const transformTime = (value) => {
  if (!value) {
    return '';
  }
  const time = new Date(value);
  return moment(time).format('YYYY/MM/DD HH:mm:ss');
};

/**
 * 将日期时间转换为 YYYY-MM-DD 格式字符串输出
 *
 * @param {number} value
 * @return {string} YYYY-MM-DD
 */
export const transformDate = (value) => {
  if (!value) {
    return '';
  }
  const time = new Date(value);
  return moment(time).format('YYYY-MM-DD');
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
  Object.keys(obj).reduce((acc, k) => {
    if (obj[k] instanceof Object) {
      return purifyDeep(obj[k]);
    }
    if (!obj[k]) {
      delete acc[k];
    }
    return acc;
  }, result);
  return result;
};

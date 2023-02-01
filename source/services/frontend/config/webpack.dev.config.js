/**
 * @description
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
/* eslint-disable */
const webpack = require('webpack');
const { merge } = require('webpack-merge');
const base = require('./webpack.base.config.js');
const { apiPrefix } = require('../src/common/utils/config');

const mock = true;

const proxy = {
  // target: 'http://124.71.133.7/',
  target: 'http://121.36.41.231:32767/',
  changeOrigin: true,
  headers: {
    Host: '121.36.41.231',
  },
};

const mockProxy = {
  target: 'http://localhost:3721/',
  changeOrigin: true,
  headers: {
    Host: 'localhost:3721',
  },
};

module.exports = merge(base, {
  mode: 'development',
  devtool: 'eval-cheap-module-source-map',
  optimization: {
    chunkIds: 'size',
  },
  devServer: {
    port: 9000,
    open: true,
    compress: true,
    proxy: {
      logLevel: 'debug',
      [apiPrefix]: mock ? mockProxy : proxy,
    },
  },
});

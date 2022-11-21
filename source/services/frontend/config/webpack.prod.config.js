/**
 * @description
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
/* eslint-disable */
const webpack = require('webpack');
const path = require('path');
const { merge } = require('webpack-merge');
const base = require('./webpack.base.config.js');

function resolve(dir) {
  return path.resolve('./', dir);
}

module.exports = merge(base, {
  mode: 'production',
  output: {
    path: resolve('dist/'),
    filename: '[name].[hash:10].js',
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
      automaticNameDelimiter: '-',
    },
  },
  devtool: false,
});

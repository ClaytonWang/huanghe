/* eslint-disable */

const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const { name } = require('../src/common/utils/config');
const devMode = process.env.NODE_ENV === 'development';

function resolve(dir) {
  return path.resolve('./', dir);
}

module.exports = {
  entry: [resolve('src/index.js')],
  output: {
    path: resolve('dist/'),
    filename: '[name].[hash:10].js',
  },
  resolve: {
    alias: {
      '@': resolve('src'),
    },
    extensions: ['.js', '.jsx', '.ts', '.tsx'],
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        include: resolve('src'),
        exclude: /node_modules/,
        use: [
          {
            loader: 'babel-loader',
            options: {
              presets: ['react-app'],
              plugins: [
                'react-require',
                ['@babel/plugin-proposal-decorators', { legacy: true }],
              ],
              // 开启babel缓存
              cacheDirectory: true,
            },
          },
        ],
      },
      {
        /** css stylesheet loader */
        test: /\.css/,
        include: resolve('src'),
        exclude: /node_modules/,
        use: [
          devMode
            ? {
                loader: 'style-loader',
              }
            : MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
          },
        ],
        // Don't consider CSS imports dead code even if the
        // containing package claims to have no side effects.
        // Remove this when webpack adds a warning or an error for this.
        // See https://github.com/webpack/webpack/issues/6571
        sideEffects: true,
      },
      {
        /** css stylesheet loader */
        test: /\.css/,
        include: resolve('node_modules'),
        use: [
          devMode
            ? {
                loader: 'style-loader',
              }
            : MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
          },
        ],
        // Don't consider CSS imports dead code even if the
        // containing package claims to have no side effects.
        // Remove this when webpack adds a warning or an error for this.
        // See https://github.com/webpack/webpack/issues/6571
        sideEffects: true,
      },
      {
        /** less stylesheet loader */
        test: /\.less$/,
        include: resolve('src'),
        // exclude: /node_modules/,
        use: [
          devMode
            ? {
                loader: 'style-loader',
              }
            : MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
          },
          {
            loader: 'less-loader',
            options: {
              lessOptions: {
                javascriptEnabled: true,
              },
            },
          },
        ],
        // Don't consider CSS imports dead code even if the
        // containing package claims to have no side effects.
        // Remove this when webpack adds a warning or an error for this.
        // See https://github.com/webpack/webpack/issues/6571
        sideEffects: true,
      },
      {
        /** iconfont loader */
        test: /(iconfont.svg)|\.(eot|ttf|woff|)w*$/,
        include: resolve('src'),
        exclude: /node_modules/,
        use: [
          {
            loader: 'url-loader',
          },
        ],
      },
      {
        /** image loader */
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'url-loader',
        options: {
          // name: '[name]_[hash].[ext]',
          limit: 3000000,
        },
      },
    ],
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: 'style/[name].[hash].css',
    }),
    new HtmlWebpackPlugin({
      title: name,
      template: resolve('public/index.html'),
      inject: true,
      minify: {
        collapseWhitespace: true,
      },
      cache: false,
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'public',
          globOptions: {
            ignore: ['**/.DS_Store', '**/index.html'],
          },
        },
      ],
    }),
  ],
};

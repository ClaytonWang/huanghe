/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-07 20:39:09
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-07 20:41:59
 * @Description
 */
module.exports = {
  success: true,
  message: '',
  result: {
    total: 50, // 总条数，数字
    data: [
      {
        id: '3', // 存储Id，字符串
        name: '约年造写示设2', // 存储名称，字符串
        config: {
          value: 0, // 当前使用容量，小于等于size，单位GB，整数
          size: 43, // 最大容量，整数（1-1024），单位GB，整数
        },
        project: {
          id: '40', // 项目ID，字符串
          name: 'ssss', // 项目名称，字符串
        },
        owner: {
          id: '60', // 用户ID，字符串
          name: 'shouchentest', // 用户名，字符串
        },
        created_at: '2022-12-14T14:07:02.946418', // 创建时间，字符串
        deleted_at: null, // 删除时间，字符串
      },
      {
        id: '2',
        name: '约年造写示设',
        config: {
          value: 0,
          size: 45,
        },
        project: {
          id: '12',
          name: 'ssss',
        },
        owner: {
          id: '60',
          name: 'shouchentest',
        },
        created_at: '2022-12-13T15:37:15.211834',
        deleted_at: null,
      },
      {
        id: '1',
        name: 'string',
        config: {
          value: 0,
          size: 0,
        },
        project: {
          id: 11,
          name: 'ssss',
        },
        owner: {
          id: '60',
          name: 'shouchentest',
        },
        created_at: '2022-12-13T11:39:54.665336',
        deleted_at: null,
      },
    ],
  },
};

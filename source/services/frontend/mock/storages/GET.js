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
        id: '1', // 存储Id，字符串
        name: 'storage-01', // 名称，字符串
        config: {
          value: 0, // 当前使用容量，小于size，单位GB，整数
          size: 10, // 最大容量，整数（1-1024），单位GB，整数
        },
        project: {
          id: 'ENG106', // 项目ID，字符串
          // code: 'EN106', // 项目编码，字符串
          name: '紫龙游戏', // 项目名称，字符串
        }, // 所属项目
        owner: {
          id: '1', // 用户ID，字符串
          username: '田政', // 用户名，字符串
        }, // 所有人
        created_at: '2022-12-06', // 创建时间，字符串
        delete_time: null, // 删除时间，字符串，如果未删除，返回null（前端判断是否小于7天）
      },
      {
        id: '2', // 存储Id，字符串
        name: 'storage-02', // 名称，字符串
        config: {
          value: 20, // 当前使用容量，小于size，单位GB，整数
          size: 200, // 最大容量，整数（1-1024），单位GB，整数
        },
        project: {
          id: 'ENG106', // 项目ID，字符串
          // code: 'EN106', // 项目编码，字符串
          name: '紫龙游戏', // 项目名称，字符串
        }, // 所属项目
        owner: {
          id: '11', // 用户ID，字符串
          username: '恒心', // 用户名，字符串
        }, // 所有人，
        created_at: '2022-11-29', // 创建时间，字符串
        delete_time: '2022-11-30', // 删除时间，字符串，如果未删除，返回null（前端判断是否小于7天）
      },
      {
        id: '3', // 存储Id，字符串
        name: 'storage-03', // 名称，字符串
        config: {
          value: 50, // 当前使用容量，小于size，单位GB，整数
          size: 100, // 最大容量，整数（1-1024），单位GB，整数
        },
        project: {
          id: 'ENG113', // 项目ID，字符串
          // code: 'EN106', // 项目编码，字符串
          name: '大模型', // 项目名称，字符串
        }, // 所属项目
        owner: {
          id: '2', // 用户ID，字符串
          username: '温颖', // 用户名，字符串
        }, // 所有人，
        created_at: '2022-12-07', // 创建时间，字符串
        delete_time: '2022-12-07', // 删除时间，字符串，如果未删除，返回null（前端判断是否小于7天）
      },
    ],
  },
};

module.exports = {
  success: true,
  message: '',
  result: {
    total: 5, // 总条数,数字
    data: [
      {
        username: '田政', // 用户名,字符串
        email: 'zheng.tian@digitalbrain.cn', // 用户邮箱,字符串；
        role: 'owner', // 角色,可选admin｜owner｜user,字符串
        project: [
          // 所属项目名称,项目对象数组
          {
            id: 'EN106',
            name: '紫龙游戏',
          },
        ],
        creatDate: '2022-10-10', // 创建时间,字符串
      },
      {
        username: '温颖', // 用户名,字符串
        email: 'ying@digitalbrain.cn', // 用户邮箱,字符串；
        role: 'owner', // 角色,可选admin｜owner｜user,字符串
        project: [
          // 所属项目名称,项目对象数组
          {
            id: 'EN107',
            name: '大模型',
          },
        ],
        creatDate: '2022-10-10', // 创建时间,字符串
      },
      {
        username: '张伟楠', // 用户名,字符串
        email: 'weinan@digitalbrain.cn', // 用户邮箱,字符串；
        role: 'owner', // 角色,可选admin｜owner｜user,字符串
        project: [
          // 所属项目名称,项目对象数组
          {
            id: 'EN108',
            name: '运筹',
          },
        ],
        creatDate: '2022-10-10', // 创建时间,字符串
      },
    ],
  },
};

module.exports = {
  data: [
    {
      username: '田政', // 用户名,字符串
      email: 'zheng.tian@digitalbrain.cn', // 用户邮箱,字符串；
      role: 'owner', // 角色,可选admin｜owner｜user,字符串
      project: [
        // 所属项目名称,项目对象数组
        {
          id: 'EN106',
          project_name: '紫龙游戏',
        },
      ],
      create_at: '2022-10-10', // 创建时间,字符串
    },
    {
      username: '温颖', // 用户名,字符串
      email: 'ying@digitalbrain.cn', // 用户邮箱,字符串；
      role: 'owner', // 角色,可选admin｜owner｜user,字符串
      project: [
        // 所属项目名称,项目对象数组
        {
          id: 'EN107',
          project_name: '大模型',
        },
      ],
      create_at: '2022-10-10', // 创建时间,字符串
    },
    {
      username: '张伟楠', // 用户名,字符串
      email: 'weinan@digitalbrain.cn', // 用户邮箱,字符串；
      role: 'owner', // 角色,可选admin｜owner｜user,字符串
      project: [
        // 所属项目名称,项目对象数组
        {
          id: 'EN108',
          project_name: '运筹',
        },
      ],
      create_at: '2022-10-10', // 创建时间,字符串
    },
  ],
};

/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-14 13:53:37
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-02-23 12:22:10
 * @FilePath: /huanghe/source/services/frontend/src/pages/overview/serverlist/ServerListTable/index.js
 * @Description: Server List Table
 */
import { useSearchParams } from 'react-router-dom';
import { Table, Tooltip } from 'antd';
import { CheckCircleFilled, CloseCircleFilled } from '@ant-design/icons';
import qs from 'qs';

const ServerListTable = ({
  tableData = {},
  loading = false,
  onPageNoChange = () => {},
}) => {
  const columns = [
    {
      title: '状态',
      dataIndex: 'status',
      width: '10%',
      render(value) {
        const icon = {
          success: (
            <Tooltip title="正常">
              <CheckCircleFilled style={{ color: '#05e087' }} />
            </Tooltip>
          ),
          error: (
            <Tooltip title="异常">
              <CloseCircleFilled style={{ color: '#ff4538' }} />
            </Tooltip>
          ),
        };
        return icon[value.toLowerCase()];
      },
    },
    {
      title: '服务器',
      dataIndex: 'server',
      width: '20%',
      render(value) {
        return value || '-';
      },
    },
    {
      title: '占用率',
      dataIndex: 'occupiedRate',
      width: '20%',
      render(value) {
        return value || '-';
      },
    },
    {
      title: '总资源规格',
      dataIndex: 'source',
      width: '20%',
    },
    {
      title: '占用人',
      dataIndex: 'occupiedBy',
      ellipsis: {
        showTitle: false,
      },
      render(value) {
        const _value = value?.map((v) => v.username).join(',');
        const tooltip = value?.reduce((prev, curr) => {
          const { tasks, username } = curr;
          return tasks.reduce((prevTask, currTask) => {
            const text = `${username} ${currTask.name} ${currTask.source}`;
            if (prevTask) {
              return `${prevTask}\n${text}`;
            }
            return text;
          }, prev);
        }, null);
        return (
          <Tooltip placement="topLeft" title={tooltip}>
            {_value}
          </Tooltip>
        );
      },
    },
  ];

  const [searchParams] = useSearchParams();
  const { pageno = 1, pagesize = 10 } = {
    ...qs.parse(searchParams.toString()),
  };

  const { total = 0, data = [] } = tableData;
  const pagination = {
    current: Number(pageno),
    pageSize: Number(pagesize),
    total,
    onChange: onPageNoChange,
    showSizeChanger: false,
  };

  return (
    <Table
      className="dbr-table"
      rowKey="id"
      size="small"
      columns={columns}
      loading={loading}
      dataSource={data}
      pagination={pagination}
    />
  );
};
export default ServerListTable;

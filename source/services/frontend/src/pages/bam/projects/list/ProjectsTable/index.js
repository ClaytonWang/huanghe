/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 12:19:26
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-01 14:14:49
 * @Description 后台管理，项目列表
 */
import { useSearchParams } from 'react-router-dom';
import { Table, Button } from 'antd';
import qs from 'qs';
import { transformDate } from '@/common/utils/helper';

const ProjectsTable = ({
  tableData = {},
  loading = false,
  onPageNoChange = () => {},
  onEdit = () => {},
  onDelete = () => {},
}) => {
  const columns = [
    {
      title: '项目编号',
      dataIndex: 'code',
    },
    {
      title: '项目名称',
      dataIndex: 'name',
    },
    {
      title: '项目负责人',
      dataIndex: 'owner',
      render(value) {
        return value.username || value;
      },
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      render(value) {
        return transformDate(value) || '-';
      },
    },
    {
      title: '操作',
      render(_value, record) {
        return (
          <span className="dbr-table-actions">
            <Button
              type="link"
              onClick={() => {
                handleEditClicked(record);
              }}
            >
              编辑
            </Button>
            <Button
              type="link"
              onClick={() => {
                handleDeleteClicked(record);
              }}
            >
              删除
            </Button>
          </span>
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
  const handleEditClicked = (record = {}) => {
    onEdit(record);
  };
  const handleDeleteClicked = (record = {}) => {
    onDelete(record);
  };
  const genTableData = (data) => data;

  return (
    <Table
      className="dbr-table"
      rowKey="id"
      size="small"
      columns={columns}
      loading={loading}
      dataSource={genTableData(data)}
      pagination={pagination}
      tableLayout="auto"
    />
  );
};
export default ProjectsTable;

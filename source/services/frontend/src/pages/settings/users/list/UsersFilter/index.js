/**
 * @description 负责人所有项目用户列表查询条件
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */

import { useMemo } from 'react';
import { Form, Input, Select, Button } from 'antd';
import { ACCESS_MAP } from '@/common/constants';
import { parseKVToKeyValue } from '@/common/utils/helper';
const { Option } = Select;

const UsersFilter = ({
  initialValues = {},
  defaultFilters = {},
  reload = () => {},
  projectsDataSource = [],
}) => {
  const [form] = Form.useForm();
  const initialFormValues = useMemo(
    () => ({
      ...initialValues,
    }),
    [initialValues]
  );
  const handleSearch = (values) => {
    reload({
      filter: {
        ...values,
      },
      pageNo: 1,
    });
  };
  const reset = () => {
    form.setFieldsValue(defaultFilters);
  };
  return (
    <Form
      form={form}
      className="list-filter"
      layout="inline"
      initialValues={initialFormValues}
      onFinish={handleSearch}
    >
      <Form.Item label="姓名" name="username">
        <Input placeholder="输入用户姓名..." style={{ width: 250 }} />
      </Form.Item>
      <Form.Item label="权限" name="access">
        <Select style={{ width: 150 }}>
          <Option key="all" value="all">
            全部
          </Option>
          {parseKVToKeyValue(ACCESS_MAP, 'k', 'v').map(({ k, v }) => (
            <Option key={k} value={k}>
              {v}
            </Option>
          ))}
        </Select>
      </Form.Item>
      <Form.Item label="所属项目" name="project">
        <Select style={{ width: 100 }}>
          <Option key="all" value="all">
            全部
          </Option>
          {projectsDataSource.map(({ id, name }) => (
            <Option key={id} value={id}>
              {name}
            </Option>
          ))}
        </Select>
      </Form.Item>
      <Form.Item className="operations">
        <Button type="primary" htmlType="submit">
          查询
        </Button>
        <Button onClick={reset}>重置</Button>
      </Form.Item>
    </Form>
  );
};
export default UsersFilter;

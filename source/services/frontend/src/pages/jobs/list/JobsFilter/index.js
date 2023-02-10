/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 16:10:19
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-01-31 16:47:47
 * @FilePath: /frontend/src/pages/jobs/list/JobsFilter/index.js
 * @Description: Job查询条件
 */
import { useMemo } from 'react';
import { Form, Input, Select, Button } from 'antd';
import { USER_ROLE } from '@/common/constants';
import { parseKVToKeyValue } from '@/common/utils/helper';
const { Option } = Select;

const NotebooksFilter = ({
  initialValues = {},
  defaultFilters = {},
  reload = () => {},
  projectsDatasource = [],
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
      pageno: 1,
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
      <Form.Item label="创建人" name="username">
        <Input placeholder="输入创建人姓名..." style={{ width: 250 }} />
      </Form.Item>
      <Form.Item label="角色" name="role__name">
        <Select style={{ width: 100 }}>
          <Option key="all" value="all">
            全部
          </Option>
          {parseKVToKeyValue(USER_ROLE, 'k', 'v').map(({ k, v }) => (
            <Option key={k} value={k}>
              {v}
            </Option>
          ))}
        </Select>
      </Form.Item>
      <Form.Item label="所属项目" name="project__code">
        <Select style={{ width: 150 }} dropdownMatchSelectWidth={false}>
          <Option key="all" value="all">
            全部
          </Option>
          {projectsDatasource.map(({ id, code, name }) => (
            <Option key={id} value={code}>
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
export default NotebooksFilter;

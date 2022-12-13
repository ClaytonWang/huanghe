/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-11-29 12:19:26
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-02 16:51:41
 * @Description 负责人所有项目用户列表查询条件
 */
import { useMemo } from 'react';
import { Form, Input, Select, Button } from 'antd';
import { USER_ROLE } from '@/common/constants';
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
      <Form.Item label="姓名" name="username">
        <Input placeholder="输入用户姓名..." style={{ width: 250 }} />
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
      <Form.Item label="所属项目" name="projects__code">
        <Select style={{ width: 150 }} dropdownMatchSelectWidth={false}>
          <Option key="all" value="all">
            全部
          </Option>
          {projectsDataSource.map(({ id, code, name }) => (
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
export default UsersFilter;

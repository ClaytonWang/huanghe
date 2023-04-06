/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2022-12-27 15:56:10
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-04-06 10:49:32
 * @FilePath: /huanghe/source/services/frontend/src/common/components/FormModal/index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
/**
 * @description 带Form表单的Modal封装，允许引用时自定义表单元素
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { Form, Modal } from 'antd';

const FormModal = ({
  title = '编辑',
  okText = '保存',
  initialValues = {},
  onSubmit,
  onCancel,
  children,
  ...rest
}) => {
  const [form] = Form.useForm();

  const handleCancelClicked = () => {
    onCancel();
    form.setFieldsValue({});
  };
  const handleOkClicked = async () => {
    const values = await form.validateFields();
    onSubmit(values);
    form.setFieldsValue({});
  };

  return (
    <Modal
      title={title}
      okText={okText}
      cancelText="取消"
      open={true}
      onOk={handleOkClicked}
      onCancel={handleCancelClicked}
      {...rest}
    >
      <Form form={form} initialValues={initialValues} layout="vertical">
        {children}
      </Form>
    </Modal>
  );
};
export default FormModal;

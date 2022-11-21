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
      visible={true}
      onOk={handleOkClicked}
      onCancel={handleCancelClicked}
    >
      <Form form={form} initialValues={initialValues} layout="vertical">
        {children}
      </Form>
    </Modal>
  );
};
export default FormModal;

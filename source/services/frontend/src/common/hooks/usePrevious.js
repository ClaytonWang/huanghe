/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2023-01-04 15:54:36
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2023-01-04 15:55:30
 * @Description previous value hook
 */
import { useEffect, useRef } from 'react';

const usePrevious = (value) => {
  const ref = useRef();
  useEffect(() => {
    ref.current = value;
  });
  return ref.current;
};
export default usePrevious;

/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2023-01-04 15:58:08
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2023-01-04 16:00:02
 * @Description location change hook
 */
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import usePrevious from './usePrevious';

const useLocationChange = (action) => {
  const location = useLocation();
  const prevLocation = usePrevious(location);
  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    action(location, prevLocation);
  }, [location]);
};
export default useLocationChange;

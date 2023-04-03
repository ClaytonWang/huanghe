/*
 * @Author: guanlin.li guanlin.li@digitalbrain.cn
 * @Date: 2023-03-17 17:12:38
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-19 23:42:02
 * @FilePath: /huanghe/source/services/frontend/src/pages/services/detail/LogList/index.js
 * @Description: 日志列表
 */
import InfiniteScroll from 'react-infinite-scroll-component';
const LogList = ({
  datasource,
  onLoadNext,
  total = null,
  pageno,
  pagesize,
}) => {
  const style = {
    height: 20,
    borderLeft: '5px solid grey',
    padding: '0 8px',
    margin: '4px 0',
    lineHeight: '20px',
  };
  const handleLoadNext = () => {
    onLoadNext({ pageno: pageno + 1, pagesize });
  };
  return (
    <div
      id="scrollableDiv"
      style={{
        height: 400,
        overflow: 'auto',
        display: 'flex',
      }}
    >
      {total > 0 && (
        <InfiniteScroll
          dataLength={datasource.length}
          next={handleLoadNext}
          hasMore={total - datasource.length > 0}
          loader={<h4>Loading...</h4>}
          scrollableTarget="scrollableDiv"
        >
          {datasource.map((content, index) => (
            <div key={index} style={style}>
              {content}
            </div>
          ))}
        </InfiniteScroll>
      )}
    </div>
  );
};
export default LogList;

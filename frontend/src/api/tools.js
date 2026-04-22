import request from './request'

// 生成词云
export function generateWordCloud(data) {
  return request({
    url: '/api/tools/wordcloud',
    method: 'post',
    data
  })
}

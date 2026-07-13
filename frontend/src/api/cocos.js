// cocos 课后出题校验 API

/**
 * 执行 verify_mastery.py，流式获取输出
 * @param {Object} data - { appoint_id, lesson_type, lesson_level }
 * @param {Function} onChunk - 每收到一段文本时的回调 (chunk: string) => void
 * @returns {Promise<void>}
 */
export async function verifyMastery(data, onChunk) {
  const response = await fetch('/api/cocos/verify_mastery', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const err = await response.json().catch(() => ({}))
    throw new Error(err.msg || `请求失败: ${response.status}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    onChunk(decoder.decode(value, { stream: true }))
  }
}

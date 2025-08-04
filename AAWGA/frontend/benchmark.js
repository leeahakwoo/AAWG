// frontend/benchmark.js
// 자동화 벤치마크: Production 번들(serve:prod)의 로드/타이핑 성능 측정

const puppeteer = require('puppeteer');

(async () => {
  const url = 'http://localhost:5000';  // serve:prod 로 띄운 포트
  // headless: 'new'를 명시해 새로운 헤드리스 모드를 사용
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  // 페이지 로드 시간 측정
  const t0 = Date.now();
  try {
    await page.goto(url, { waitUntil: 'networkidle0' });
  } catch (err) {
    console.error(`페이지 접속 실패: ${url}`, err);
    await browser.close();
    process.exit(1);
  }
  await page.waitForSelector('.editor-input');
  console.log('Production Load time:', Date.now() - t0, 'ms');

  // 타이핑 벤치 (약 114자)
  await page.click('.editor-input');
  const text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. '.repeat(2);
  const t1 = Date.now();
  await page.keyboard.type(text);
  console.log(`Production Typing ${text.length} chars time:`, Date.now() - t1, 'ms');

  await browser.close();
})();

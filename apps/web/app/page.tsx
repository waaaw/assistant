export default function HomePage() {
  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">AI EXECUTIVE ASSISTANT</p>
          <h1>오늘의 업무 허브</h1>
        </div>
        <span className="status"><i /> 시스템 준비됨</span>
      </header>
      <section className="intro">
        <p className="date">2026년 7월 11일 토요일</p>
        <h2>중요한 일부터 선명하게.</h2>
        <p className="muted">캘린더, 업무, 알림을 한곳에서 확인하는 개인 비서 공간입니다.</p>
      </section>
      <section className="grid" aria-label="업무 요약">
        <article><span>오늘 일정</span><strong>연동 대기</strong><p>Google Calendar 연결 후 표시됩니다.</p></article>
        <article><span>처리할 승인</span><strong>0건</strong><p>외부 변경은 항상 승인 후 실행됩니다.</p></article>
        <article><span>상태 점검</span><strong>MP-00</strong><p>기본 웹 화면이 정상적으로 동작합니다.</p></article>
      </section>
    </main>
  );
}


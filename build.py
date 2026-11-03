"""Build the UtterAI case study for GitHub Pages (standard library only)."""
from pathlib import Path
from html import escape
import hashlib
import struct

ROOT = Path(__file__).parent
ORIGIN = 'https://gpffh20.github.io'
REPOSITORY = 'https://github.com/UtterAI-aws13/UtterAI_Infra'
BRANCH = 'eunyoung/infra-lab'
SOURCE = f'{REPOSITORY}/tree/{BRANCH}'


def figure(filename, alt, caption, extra_class=''):
    width, height = struct.unpack('>II', (ROOT / 'assets' / filename).read_bytes()[16:24])
    return f'''<figure class="figure {extra_class}">
      <button type="button" data-enlarge aria-label="{escape(alt)} 확대 보기">
        <img src="/assets/{filename}" alt="{escape(alt)}" width="{width}" height="{height}" loading="lazy">
      </button><figcaption>{caption} · 클릭하여 확대</figcaption>
    </figure>'''


def code_links(title, items):
    links = ''
    for path, label in items:
        kind = 'blob' if Path(path).suffix else 'tree'
        url = f'{REPOSITORY}/{kind}/{BRANCH}/{path}'
        links += f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span></a>'
    return f'<aside class="code-links" aria-label="{title}"><span>{title}</span><div>{links}</div></aside>'


css_version = hashlib.sha256((ROOT / 'styles.css').read_bytes()).hexdigest()[:10]
js_version = hashlib.sha256((ROOT / 'site.js').read_bytes()).hexdigest()[:10]
cases = (ROOT / 'templates' / 'utterai-cases.html').read_text()
references = {
    'network': [('terraform/environments/prod/01-network/main.tf', '네트워크 구성'), ('terraform/environments/prod/02-eks/main.tf', 'EKS 설정')],
    'scaling': [('k8s/apps/ai-worker/overlays/prod', 'KEDA 설정'), ('components/capacity-policy/policy.py', '배치 정책 구현'), ('k8s/platform/karpenter/base/nodepools.yaml', 'NodePool 구성')],
    'chatops': [('components/slack-llm-worker/slack_worker', 'Worker 구현'), ('components/slack-llm-worker/docs/chatops-verification.md', 'ChatOps 검증 기록'), ('components/slack-llm-worker/evidence/gitops-e2e.json', 'GitOps 검증 기록')],
}
for section_id, items in references.items():
    start = cases.index(f'id="{section_id}"')
    end = cases.index('</section>', start)
    cases = cases[:end] + code_links('구현 코드 · 관련 기록', items) + cases[end:]

body = (ROOT / 'templates' / 'home.html').read_text()
body = body.replace('{{ARCHITECTURE}}', figure('utterai-architecture.png', 'UtterAI 전체 시스템 아키텍처', 'EKS 기반 비동기 AI 처리 파이프라인과 운영 구성', 'architecture'))
body = body.replace('{{CASE_STUDIES}}', cases)
title = 'UtterAI 기술 포트폴리오 | 신은영'
description = 'EKS 기반 AI 임상 어시스턴트 UtterAI의 네트워크 장애 해결, 큐 기반 오토스케일링과 비용 최적화, Slack ChatOps 구현·검증 기록.'
page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{description}">
<meta name="theme-color" content="#fafafa"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:url" content="{ORIGIN}/">
<link rel="canonical" href="{ORIGIN}/"><link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="preload" href="/assets/PretendardVariable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css?v={css_version}"><script src="/site.js?v={js_version}" defer></script></head>
<body><a class="skip" href="#main">본문으로 건너뛰기</a>
<header class="site-header"><div class="wrap header-inner"><a class="brand" href="/#main">UtterAI<span>신은영 · DevOps</span></a>
<nav class="main-nav" aria-label="목차"><a href="#overview">개요</a><a href="#architecture">아키텍처</a><a href="#cases">문제 해결</a><a href="#resources">자료</a></nav></div></header>
<main class="wrap" id="main">{body}</main>
<footer class="wrap footer"><div><strong>신은영</strong><span>Team Lead / DevOps Engineer</span></div><a href="mailto:eunice.shin54@gmail.com">eunice.shin54@gmail.com ↗</a><a href="#main">맨 위로 ↑</a></footer>
<dialog class="lightbox" id="image-dialog" aria-label="이미지 확대 보기"><button type="button" class="lightbox-close" aria-label="이미지 닫기">닫기 ×</button><img alt=""></dialog>
</body></html>'''
(ROOT / 'index.html').write_text(page)

# Preserve old project URLs without maintaining duplicate portfolio pages.
for slug in ('utterai', 'migration', 'disasterkok'):
    directory = ROOT / 'projects' / slug
    directory.mkdir(parents=True, exist_ok=True)
    preserve_hash = 'location.hash' if slug == 'utterai' else "''"
    directory.joinpath('index.html').write_text(f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>UtterAI 기술 포트폴리오</title><meta name="robots" content="noindex,follow"><link rel="canonical" href="{ORIGIN}/"><script>location.replace('/' + {preserve_hash});</script></head><body><a href="/">UtterAI 기술 포트폴리오로 이동 →</a></body></html>''')

(ROOT / '404.html').write_text(f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>페이지를 찾을 수 없습니다 | UtterAI</title><link rel="stylesheet" href="/styles.css?v={css_version}"></head><body><main class="wrap hero"><div class="eyebrow">404</div><h1>페이지를 찾을 수 없습니다.</h1><p>주소를 확인하거나 포트폴리오 첫 화면으로 이동해주세요.</p><a class="text-link" href="/">UtterAI 포트폴리오 →</a></main></body></html>''')
(ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
(ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{ORIGIN}/</loc></url></urlset>')
print('Built UtterAI portfolio, compatibility routes, 404 and sitemap.')

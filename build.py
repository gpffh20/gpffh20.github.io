from pathlib import Path
from html import escape
import struct
import hashlib

DIST = Path(__file__).parent
CSS_VERSION = hashlib.sha256((DIST / 'styles.css').read_bytes()).hexdigest()[:10]
ORIGIN = 'https://gpffh20.github.io'
GITHUB = 'https://github.com/gpffh20'
UTTERAI = 'https://github.com/UtterAI-aws13/UtterAI_Infra/tree/eunyoung/infra-lab'
MIGRATION = 'https://github.com/2026-Softbank-hackathon'
DISASTER = 'https://github.com/gpffh20/Disasterkok'

def external(url, label, cls='text-link'):
    return f'<a class="{cls}" href="{url}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span></a>'

def tags(*items):
    return '<div class="tags">' + ''.join(f'<span class="tag">{escape(item)}</span>' for item in items) + '</div>'

def figure(file, alt, caption, cls=''):
    width, height = struct.unpack('>II', (DIST / 'assets' / file).read_bytes()[16:24])
    return f'<figure class="figure {cls}"><button type="button" data-enlarge aria-label="{escape(alt)} 확대 보기"><img src="/assets/{file}" alt="{escape(alt)}" width="{width}" height="{height}" loading="lazy"></button><figcaption>{caption} · 클릭하여 확대</figcaption></figure>'

def results(*items):
    return '<div class="results">' + ''.join(f'<div class="result"><strong>{value}</strong><span>{label}</span></div>' for value,label in items) + '</div>'

def flow(*items):
    cells=[]
    for title,subtitle in items:
        if cells: cells.append('<span class="flow-arrow" aria-hidden="true">→</span>')
        cells.append(f'<div class="flow-step"><strong>{title}</strong><span>{subtitle}</span></div>')
    return '<div class="flow">'+''.join(cells)+'</div>'

def layout(title, description, body, page='', nav=None):
    is_home = not page
    links=''.join(f'<a href="{"" if is_home else "/"}#{id}">{label}</a>' for id,label in [('projects','Projects'),('experience','Experience'),('education','Education'),('skills','Skills')])
    toc = '' if is_home or not nav else '<nav class="article-nav" aria-label="프로젝트 목차">'+''.join(f'<a href="#{id}">{label}</a>' for id,label in nav)+'</nav>'
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description)}">
<meta name="theme-color" content="#f0f3ed"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{ORIGIN}/{page}">
<link rel="canonical" href="{ORIGIN}/{page}"><link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="preload" href="/assets/PretendardVariable.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/styles.css?v={CSS_VERSION}"><script src="/site.js" defer></script></head>
<body><a class="skip" href="#main">본문으로 건너뛰기</a>
<header class="site-header"><div class="nav-wrap"><a class="brand" href="/" aria-label="신은영 포트폴리오 홈">Eunice Shin<span> · DevOps Engineer</span></a><nav class="main-nav" aria-label="메인 메뉴">{links}</nav></div></header>
<main class="main {"home" if is_home else "article"}" id="main">{toc}{body}<footer class="footer"><span>© 2026 신은영 · Eunice Shin</span><div><a href="/assets/eunice-shin-resume.pdf" download="신은영_이력서.pdf">이력서 PDF ↓</a><a href="#main">맨 위로 ↑</a></div></footer></main>
<dialog class="lightbox" id="image-dialog" aria-label="이미지 확대 보기"><button type="button" class="lightbox-close" aria-label="이미지 닫기">닫기 ×</button><img alt=""></dialog>
</body></html>'''

def article_header(name, subtitle, period, role, team, skills, links, award=''):
    return f'''<div class="breadcrumb"><a href="/#projects">← 프로젝트 목록</a><span>/</span><span>{name}</span></div>
<header class="article-hero"><div class="eyebrow">PROJECT / CASE STUDY</div><h1>{name}</h1><p class="lead">{subtitle}</p>
{f'<span class="award">{award}</span>' if award else ''}<div class="article-meta"><span><strong>기간</strong>{period}</span><span><strong>역할</strong>{role}</span><span><strong>팀</strong>{team}</span></div>
{tags(*skills)}<div class="article-actions">{links}</div></header>'''

home = (Path(__file__).parent / 'templates' / 'home.html').read_text(encoding='utf-8')

utterai=article_header('UtterAI','AI 기반 언어치료 임상 어시스턴트의 인프라를 설계하고, 장애 진단부터 비용 최적화와 복구 검증까지 개선했습니다.','2026.05 – 2026.07','Team Lead / DevOps Engineer','4인', ['AWS EKS','Terraform','SQS','KEDA','Karpenter','Argo CD','LiteLLM'],external(UTTERAI,'GitHub','button')+external('https://youtu.be/4a5bOTO9fbY','서비스 데모','button'),'AWS Cloud School 최종 프로젝트 최우수상')+f'''
<section class="article-section" id="overview"><div class="section-number">00 / OVERVIEW</div><h2>서비스와 담당 역할</h2><p>언어재활사가 치료 세션 녹음을 업로드하면, 발화자를 구분한 전사문과 언어지표를 분석하고 SOAP 형식의 치료 기록 초안을 생성하는 서비스입니다. 치료사는 분석 결과와 초안을 검토·수정해 치료 기록을 완성합니다.</p><p>4인 팀 리드로 업무 분장, 일일 회의와 일정 관리를 주도하고 기술적 의사결정을 지원했습니다. 인프라 영역에서는 EKS 네트워크, 큐 기반 오토스케일링, GitOps 배포와 Slack 기반 장애 대응 흐름을 구성했습니다.</p>
{results(('약 58% ↓','EC2 Compute 일비용 · $28.73 → $12.02'),('33초','롤백 PR merge 이후 복구 여부 확인'))}
<h3>전체 아키텍처</h3><p>단계별 SQS 큐와 CPU·GPU Worker로 AI 처리 파이프라인을 구성했습니다. KEDA는 작업량에 따라 Pod 수를 조정하고, Karpenter는 필요한 Node를 공급합니다. GitHub Actions·Terraform·Argo CD를 배포 흐름에 연결하고 관측 지표와 ChatOps로 운영 상태를 확인했습니다.</p>
{figure('utterai-architecture.png','UtterAI 전체 시스템 아키텍처','AWS EKS 기반 비동기 AI 처리 파이프라인과 운영 구성','architecture')}
<div class="article-toc"><a href="#network">01. IP가 남아 있는데도 Pod를 만들 수 없었던 이유 →</a><a href="#scaling">02. 작업량에 맞춘 오토스케일링과 비용 최적화 →</a><a href="#chatops">03. 장애 조사부터 승인형 복구 검증까지 이어지는 ChatOps →</a></div></section>

<section class="article-section" id="network"><div class="section-number">01 / NETWORK TROUBLESHOOTING</div><h2>IP가 남아 있는데도 Pod를 만들 수 없었던 이유</h2><div class="callout">남은 IP의 개수와 할당 가능한 주소 블록은 달랐습니다. IPAMD 로그로 Prefix 할당 실패를 확인하고, Node와 Pod의 주소 영역을 분리했습니다.</div>
{figure('network-isolation.png','변경 전 Node·Pod 공유 서브넷과 변경 후 Secondary CIDR 기반 Pod 전용 서브넷 비교','문제 서브넷에서 Pod 전용 주소 영역으로 분리')}
<h3>문제와 원인</h3><p>CPU Worker가 <code>ContainerCreating</code> 상태에 머무르며 Pod IP 할당에 실패했습니다. 서브넷에는 가용 IP가 112개 남아 있어 단순한 IP 소진만으로 설명하기 어려웠습니다.</p><p>Pod 이벤트와 Node ENI 상태를 확인한 뒤 VPC CNI·IPAMD 로그를 추적해 <code>InsufficientCidr</code> 오류를 확인했습니다. Prefix Delegation은 정렬된 /28 블록 단위로 주소를 할당하는데, VPC Endpoint ENI와 Node별 예비 Prefix로 인해 서브넷이 단편화되어 할당 가능한 /28 블록이 남지 않았습니다.</p>
<h3>해결 과정</h3><ul><li>Secondary CIDR <code>100.64.0.0/16</code>에 AZ별 Pod 전용 서브넷을 만들고 Custom Networking으로 Node·Pod 주소 영역을 분리했습니다.</li><li>AZ별 ENIConfig를 연결하고, Karpenter의 Node 서브넷 탐색 대상에서 Pod 서브넷을 제외했습니다.</li><li>이후 DNS 조회 실패를 양쪽 Node의 tcpdump로 추적해 보안 그룹 단계의 차단으로 좁혔습니다. Pod용 ENI와 CoreDNS Node 간 상호 허용 규칙을 추가했습니다.</li><li>기존 VPC 대역만 허용하던 VPC Endpoint 보안 그룹에 Pod 대역을 추가해 SQS 연결 실패를 해결했습니다.</li></ul>
<h3>결과와 확인</h3><p>새 Pod가 <code>100.64.x.x</code> 대역의 IP를 받아 ContainerCreating 상태를 벗어났습니다. Pod 할당 가능 주소를 AZ당 약 250개에서 약 3.2만 개로 확장하고, Node 서브넷은 Node당 IP 1개만 사용하는 구조로 바꿨습니다.</p></section>

<section class="article-section" id="scaling"><div class="section-number">02 / WORKLOAD-DRIVEN AUTOSCALING</div><h2>작업량에 맞춰 확장하고, 기본 용량은 보호하기</h2><div class="callout">KEDA는 “얼마나 늘릴지”, 배치 정책은 “어디에 둘지”, Karpenter는 “어떤 Node를 공급할지”를 담당하도록 역할을 나눴습니다.</div>
{figure('autoscaling.png','SQS 작업량 기반 KEDA 스케일링과 Mutating Webhook의 Base·Burst 배치, Karpenter Node 공급 흐름','SQS Queue Depth → Pod 수 조정 → Base·Burst 배치 → Node 공급')}
<h3>기존 구조의 한계</h3><ul><li>CPU 사용률 70% 기준 HPA가 GPU 연산 부하와 SQS 대기량 증가를 감지하지 못해 Scale-out이 되지 않았습니다.</li><li>최소 replica가 1이어서 요청이 없어도 GPU·Batch가 상시 실행되었습니다.</li><li>Spot 도입 시 기본 처리 용량까지 회수될 위험이 있었고, GPU를 0개로 축소하면 첫 요청이 Node 공급과 모델 기동을 약 5분 기다렸습니다.</li></ul>
<h3>1. SQS 작업량을 기준으로 확장</h3><p>KEDA로 확장 기준을 CPU에서 SQS로 바꾸고 visible·in-flight 메시지를 합산해 처리 중인 작업이 지표에서 누락되지 않도록 했습니다. 워크로드별 목표 큐 길이와 min/max replica를 설정하고, Pod가 Pending 상태가 되면 Karpenter가 CPU·GPU 요구사항에 맞는 Node를 공급하도록 구성했습니다.</p>
<h3>2. 기본 용량과 추가 용량의 배치 분리</h3><p>Base는 On-Demand 전용 NodePool에, Burst는 Spot을 선호하되 공급이 부족하면 On-Demand도 허용하는 NodePool에 배치했습니다. 단일 Deployment에 Mutating Webhook을 적용해 KEDA가 정한 Pod 수를 유지하면서 각 Pod의 배치 조건을 구분했습니다.</p><ul><li>ConfigMap 예약과 resourceVersion 기반 충돌 재시도로 여러 웹훅 복제본이 Base를 중복 배정하지 않도록 했습니다.</li><li>원본 Pod 템플릿을 On-Demand로 두고 <code>failurePolicy: Ignore</code>를 적용해 웹훅 장애 중에도 Pod 생성이 가능하도록 구성했습니다.</li><li>pod-deletion-cost로 같은 ReplicaSet에서 Burst가 먼저 삭제되도록 유도했습니다.</li></ul>
<h3>3. 유휴 비용과 첫 요청 대기시간의 균형</h3><p>Batch·GPU는 기본적으로 min replica를 0으로 설정했습니다. GPU는 평일 08:30–20:00에 KEDA Cron으로 1개를 미리 띄우고, 업무 외 시간에는 0개로 축소해 첫 요청 대기와 유휴 비용을 함께 고려했습니다.</p>
<h3>4. 축소와 Spot 중단에 대응</h3><p>EventBridge와 중단 이벤트 전용 SQS로 Karpenter가 Spot 중단 경고를 받도록 구성했습니다. Worker 종료 시 새 작업 수신을 중단하고 진행 중인 작업을 마무리하며, 강제 종료된 작업은 SQS visibility가 만료되면 다시 수신하도록 했습니다. CPU·GPU Worker의 빈 Node만 정리해 실행 중인 작업을 보호했습니다.</p>
<h3>결과와 검증</h3>{results(('$28.73 → $12.02','EC2 Compute 일비용 · 약 58% 절감'),('168h → 57.5h','GPU 주간 기본 유지 시간'))}<p>Grafana에서 Worker별 desired·available replica를 비교해 실제 확장·축소 동작을 확인했습니다.</p>{figure('grafana-scaling.png','Grafana에 기록된 Worker별 목표 replica와 가용 replica 변화','Worker별 목표·가용 replica 변화')}
<p class="evidence-note">비용 수치는 프로젝트에서 오토스케일링·Spot·인스턴스 구성을 조정한 전후 EC2 Compute 일비용입니다. 전체 AWS 비용 절감률과 구분합니다.</p></section>

<section class="article-section" id="chatops"><div class="section-number">03 / INCIDENT RESPONSE & CHATOPS</div><h2>장애 조사부터 승인형 복구 검증까지</h2><div class="callout">장애 근거를 모아 롤백 PR을 제안하고, 운영자가 승인·merge한 뒤 새 이미지의 Pod 상태까지 확인해 같은 Slack 스레드에 결과를 남겼습니다.</div>
{figure('chatops.png','Slack·Lambda·SQS·ECS Worker·LiteLLM과 GitHub·Argo CD를 연결한 ChatOps 구조','요청 처리와 GitOps 기반 복구 검증 흐름')}
<h3>문제</h3><p>단계별 큐와 Worker로 나뉜 파이프라인에서 장애를 조사하려면 큐 상태, Pod 이벤트, 최근 배포 이력을 따로 확인해야 했습니다. 롤백 이후에도 새 버전 반영과 Pod 정상 동작을 수동으로 확인하고 팀에 다시 알려야 했습니다.</p><p>Slack의 3초 응답 제한보다 LLM 응답이 오래 걸리면 요청이 재전달되어 모델 호출과 답글이 중복될 수 있었습니다. 질의응답과 장애 분석은 응답 속도·입력량·허용 비용도 달랐습니다.</p>
<h3>1. 알림에 원인 배포 정보 연결</h3><p>알림·배포 이벤트·운영자 명령을 하나의 큐로 받아 처리하고, 실제 Pod의 이미지 태그를 배포 저장소 커밋과 연결했습니다. 배포가 원인인 경우 규칙에 따라 롤백 PR 생성 버튼을 제공했습니다.</p>
<h3>2. Merge 이벤트로 복구 확인 시작</h3><p>롤백 PR의 merge 이벤트를 받아 Argo CD 동기화, 새 이미지 Pod의 Ready 상태와 재시작 횟수를 차례로 확인했습니다. Rolling update 중 기존 Pod 때문에 Ready 수가 정상으로 보일 수 있어 새 이미지의 Pod를 기준으로 판정했습니다.</p>
<h3>3. 요청 접수와 비동기 처리 분리</h3><p>Lambda는 요청 서명을 검증하고 SQS에 넣은 뒤 즉시 응답합니다. Worker는 요청별 처리 상태와 생성 결과를 DynamoDB에 저장해 재전달 시 재사용하고, 전송 결과가 불확실한 답글은 중복 전송하지 않도록 처리했습니다.</p>
<h3>4. LiteLLM으로 모델·호출·비용 정책 분리</h3><p>서비스별 키에 허용 모델, 분당 호출 수와 예산을 지정하고 질의응답은 빠른 모델, 장애 요약은 큰 모델로 고정했습니다. Redis로 프록시 간 호출 한도를 공유하고 모델에 도달하지 않은 실패는 재시도 횟수에서 제외했습니다.</p>
<h3>결과</h3>{results(('6초 이내','장애 알림 후 원인 배포 커밋 표시'),('33초','롤백 PR merge 후 복구 여부 확인'),('6.6초 → 2.4초','Haiku로 분리한 질의응답 시간'),('1/3','질의응답 호출 비용'))}<ul><li>같은 요청이 3번 재전달되어도 모델 호출과 답글은 1번만 실행됐습니다.</li><li>봇의 단독 merge 시도는 HTTP 405로 차단해 운영자가 승인한 롤백만 반영되도록 했습니다.</li></ul><p class="evidence-note">응답·복구 시간과 중복 처리 결과는 프로젝트 검증 시나리오에서 확인한 값입니다.</p></section>

<section class="article-section" id="delivery"><div class="section-number">04 / DELIVERY & OTHER CONTRIBUTIONS</div><h2>배포와 협업</h2><ul><li>App of Apps·Argo CD 기반 dev/prod GitOps 배포를 구성하고 KEDA와의 replica 관리 충돌을 해결했습니다.</li><li>Amazon Bedrock·Strands Agents 기반 5-Agent 임상 리포트 생성 파이프라인을 구축했습니다.</li><li>팀 리드로 진행 지연 원인을 해결하고 업무 분장·일일 회의·일정 관리와 기술적 의사결정을 지원했습니다.</li></ul><div class="download-row">{external(UTTERAI,'소스 코드 확인')}<a href="/assets/eunice-shin-portfolio.pdf" download="신은영_포트폴리오.pdf">원본 포트폴리오 PDF ↓</a></div></section>
<div class="next-project"><a class="text-link" href="/">← 프로젝트 목록</a><a href="/projects/migration/"><span>NEXT PROJECT</span><strong>코로의 이사 ↗</strong></a></div>
'''

migration=article_header('코로의 이사','클라우드와 온프레미스 사이에서 애플리케이션을 옮기고, 같은 URL로 전환 결과를 확인하는 이식 자동화 플랫폼입니다.','2026.09 – 2026.10','Cloud Engineer','6인',['Terraform','AWS ECS Fargate','ECR','VPC','ALB','IAM','S3','Docker','Cloudflare','SOPS'],external(MIGRATION,'GitHub','button')+external('https://youtu.be/Ed6JODQt9sQ','서비스 데모','button'))+f'''
<section class="article-section" id="overview"><div class="section-number">00 / OVERVIEW</div><h2>담당 범위</h2><p>Cloud Engineer로 Terraform 기반 AWS 인프라 프로비저닝, 이미지 갱신 배포 최적화, Agent용 ECR 단기 인증 API와 Cloudflare Origin 연동을 담당했습니다.</p>{flow(('Infrastructure','Terraform 기반 프로비저닝'),('Migration','AWS ↔ On-Prem 전환'),('Verification','고정 URL로 결과 검증'))}<div class="callout">이식 후 서비스 응답만 확인하는 데서 그치지 않고, 이미지 digest와 실제 실행 호스트를 대조해 의도한 환경에서 배포되었는지 검증했습니다.</div></section>

<section class="article-section" id="optimization"><div class="section-number">01 / DEPLOYMENT OPTIMIZATION</div><h2>이미지 갱신에 필요한 작업만 수행하기</h2><h3>개선 대상</h3><p>Terraform 기반 배포 실행 경로에서 이미지 갱신 시 반복되는 준비·검증 작업을 줄였습니다.</p><h3>수행한 변경</h3><ul><li>Terraform 작업 폴더를 재사용하도록 구성했습니다.</li><li>중복 초기화와 검증 작업을 생략해 이미지 갱신에 필요한 실행 경로를 줄였습니다.</li></ul>{results(('약 72% ↓','이미지 갱신 배포 시간 단축'),('Terraform','인프라 프로비저닝 자동화'))}<p class="evidence-note">72%는 이미지 갱신 배포의 전후 비교 수치입니다. 전체 인프라 최초 구축 시간과 구분합니다.</p></section>

<section class="article-section" id="security"><div class="section-number">02 / CREDENTIAL DESIGN</div><h2>Agent에 장기 AWS 키를 전달하지 않기</h2><p>Terraform 인프라 프로비저닝에 SOPS 기반 Zero-Secret 패턴을 적용했습니다. Agent용 ECR 단기 인증 API는 Job 소유권과 lease를 검증한 뒤 인증을 제공하도록 구현해 장기 AWS 키를 Agent에 전달하지 않도록 했습니다.</p><h3>담당 구현</h3><ul><li>SOPS를 활용한 인프라 비밀 정보 관리 패턴 적용</li><li>요청 Agent의 Job 소유권과 lease 검증</li><li>ECR 접근용 단기 인증 API 구현</li></ul></section>

<section class="article-section" id="verification"><div class="section-number">03 / MIGRATION VERIFICATION</div><h2>같은 URL에서 실행 환경까지 확인하기</h2><p>Cloudflare Origin 연동으로 고정 URL 기반 AWS ↔ On-Prem 전환을 구현하고 검증했습니다. 환경 전환 뒤 서비스 응답, 이미지 digest와 실행 호스트를 대조해 배포 결과를 확인했습니다.</p><div class="callout"><strong>확인한 세 가지</strong><br>서비스가 응답하는가 → 의도한 이미지가 실행되는가 → 전환한 대상 호스트에서 실행되는가</div><div class="download-row">{external(MIGRATION,'프로젝트 소스 코드')}{external('https://youtu.be/Ed6JODQt9sQ','데모 영상')}<a href="/assets/eunice-shin-resume.pdf" download="신은영_이력서.pdf">이력서 PDF ↓</a></div></section>
<div class="next-project"><a class="text-link" href="/">← 프로젝트 목록</a><a href="/projects/disasterkok/"><span>NEXT PROJECT</span><strong>재난콕 ↗</strong></a></div>
'''

disaster=article_header('재난콕','재난 상황에서 사용자 제보를 기반으로 지역별 재난 정보를 공유하는 플랫폼입니다. 초기 팀 프로젝트 이후 성능과 인프라를 개인적으로 고도화했습니다.','2023.08 – 2024.07 / 2026.03 – 2026.09','Backend / Infra','6인 → 개인 고도화',['Django','PostgreSQL','Redis','Celery','ECS Fargate','RDS','Terraform','GitHub Actions'],external(DISASTER,'GitHub','button')+external('https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11862329','관련 논문','button'),'KCC 학부생·주니어 논문 경진대회 장려상')+f'''
<section class="article-section" id="overview"><div class="section-number">00 / OVERVIEW</div><h2>서비스와 개선 방향</h2><p>사용자가 제보한 지역별 재난 정보를 공유하는 서비스입니다. 6인 팀에서 Backend·Infra를 맡았고, 이후 개인 고도화 과정에서 부하 테스트로 병목을 확인하고 컴퓨트 아키텍처와 배포 방식을 개선했습니다.</p><div class="callout">부하 테스트로 병목을 찾고, 캐시·비동기 처리와 실행 환경 전환을 통해 성능과 배포 흐름을 개선했습니다.</div></section>

<section class="article-section" id="performance"><div class="section-number">01 / PERFORMANCE</div><h2>측정으로 병목을 찾고 처리 방식을 나누기</h2><p>부하 테스트로 병목 구간을 식별한 뒤 Redis 캐싱과 Celery 비동기 큐를 적용했습니다.</p>{flow(('Load Test','병목 구간 식별'),('Redis / Celery','캐싱·비동기 큐 적용'),('Result','p95 지연시간 단축'))}{results(('75% ↓','부하 테스트 기준 p95 지연시간'),('Redis · Celery','캐싱과 비동기 작업 처리'))}<p class="evidence-note">75%는 프로젝트 부하 테스트에서 확인한 p95 지연시간의 전후 비교 수치입니다.</p></section>

<section class="article-section" id="infrastructure"><div class="section-number">02 / COMPUTE ARCHITECTURE</div><h2>단일 노드의 자원 제약 분석과 아키텍처 전환</h2><p>메모리와 I/O 지표를 바탕으로 단일 노드 k3s의 자원 제약을 분석하고, 컴퓨트 아키텍처를 ECS Fargate로 전환했습니다.</p><h3>사용한 구성</h3><ul><li>AWS ECS Fargate · RDS · EC2</li><li>Django · PostgreSQL · Redis · Celery</li><li>Terraform 기반 인프라 코드화</li></ul></section>

<section class="article-section" id="delivery"><div class="section-number">03 / DELIVERY AUTOMATION</div><h2>인프라와 배포를 코드로 관리하기</h2><p>Terraform으로 인프라를 코드화하고 GitHub Actions에 OIDC를 적용했습니다. 이를 기반으로 무중단 배포를 자동화했습니다.</p><div class="download-row">{external(DISASTER,'프로젝트 소스 코드')}{external('https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11862329','관련 논문 확인')}<a href="/assets/eunice-shin-resume.pdf" download="신은영_이력서.pdf">이력서 PDF ↓</a></div></section>
<div class="next-project"><a class="text-link" href="/">← 프로젝트 목록</a><a href="/projects/utterai/"><span>FEATURED PROJECT</span><strong>UtterAI ↗</strong></a></div>
'''

pages=[
 ('index.html',layout('신은영 | DevOps Engineer','로그와 지표로 장애를 진단하고, 운영 구조를 개선하는 데브옵스 엔지니어 신은영의 포트폴리오.',home)),
 ('projects/utterai/index.html',layout('UtterAI | 신은영 포트폴리오','EKS 네트워크 장애 해결, KEDA·Karpenter 기반 비용 최적화, Slack ChatOps와 승인형 복구 검증.',utterai,'projects/utterai/',[('overview','프로젝트 소개'),('network','네트워크 장애'),('scaling','오토스케일링'),('chatops','Slack ChatOps'),('delivery','배포와 협업')])),
 ('projects/migration/index.html',layout('코로의 이사 | 신은영 포트폴리오','Terraform 기반 클라우드·온프레미스 이식 자동화, 배포 시간 단축과 ECR 단기 인증 구현.',migration,'projects/migration/',[('overview','프로젝트 소개'),('optimization','배포 최적화'),('security','단기 인증'),('verification','전환 검증')])),
 ('projects/disasterkok/index.html',layout('재난콕 | 신은영 포트폴리오','부하 테스트 기반 성능 개선, ECS Fargate 전환과 Terraform·GitHub Actions 배포 자동화.',disaster,'projects/disasterkok/',[('overview','프로젝트 소개'),('performance','성능 개선'),('infrastructure','인프라 전환'),('delivery','배포 자동화')])),
]
for name,content in pages:
    path=DIST/name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content,encoding='utf-8')
(DIST/'404.html').write_text(layout('페이지를 찾을 수 없습니다 | 신은영','신은영 포트폴리오 홈으로 돌아가세요.','<section class="hero"><div class="hero-tag">404 / PAGE NOT FOUND</div><h1>페이지를 찾을 수 없습니다.</h1><p class="hero-intro">주소를 확인하거나 포트폴리오 홈으로 돌아가주세요.</p><a class="button primary" href="/">포트폴리오 홈으로 →</a></section>',page='404.html',nav=[]),encoding='utf-8')
(DIST/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')
(DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}/{p}</loc></url>' for p in ['','projects/utterai/','projects/migration/','projects/disasterkok/'])+'</urlset>')
print('Generated 4 portfolio pages, 404, sitemap and robots.txt')

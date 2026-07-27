from datetime import date

from django.core.management.base import BaseCommand

from profiles.models import Profile, Skill, SkillCategory, TimelineEntry
from projects.models import Project


class Command(BaseCommand):
    help = '데모용 프로필/타임라인/기술스택/프로젝트 샘플 데이터를 생성합니다.'

    def handle(self, *args, **options):
        profile, created = Profile.objects.get_or_create(
            email='jhlim244@naver.com',
            defaults=dict(
                name_ko='임재혁',
                name_en='jaehyeok Lim',
                role_ko='임베디드 소프트웨어 엔지니어',
                role_en='Embedded Software Engineer',
                tagline_ko='하드웨어와 대화하는 소프트웨어를 만듭니다.',
                tagline_en='Building software that talks to hardware.',
                bio_ko=(
                    '센서와 통신 프로토콜 사이의 타이밍을 맞추고, 제한된 자원 안에서 안정적으로 동작하는 '
                    '펌웨어를 설계합니다. 모터 제어, 저전력 IoT, 산업용 통신 게이트웨이가 주 무대입니다.'
                ),
                bio_en=(
                    'I design firmware that stays reliable under tight resource constraints, '
                    'bridging sensors and communication protocols with precise timing. '
                    'Motor control, low-power IoT, and industrial gateways are my main stage.'
                ),
                location='Seoul, Korea',
                github_url='https://github.com/jaehyeok',
            ),
        )
        self.stdout.write(self.style.SUCCESS(f'Profile {"created" if created else "already exists"}'))

        timeline_data = [
            dict(
                category='work', order=1,
                title_ko='선임 연구원 · 스마트팩토리 솔루션팀', title_en='Senior Engineer, Smart Factory Solutions Team',
                description_ko='산업용 CAN/Modbus 게이트웨이 및 모터 제어 펌웨어 개발 총괄',
                description_en='Led development of industrial CAN/Modbus gateways and motor control firmware',
                start_date=date(2021, 3, 1), end_date=None,
            ),
            dict(
                category='work', order=2,
                title_ko='연구원 · IoT 디바이스팀', title_en='Engineer, IoT Device Team',
                description_ko='배터리 구동 센서 노드용 저전력 펌웨어 및 BLE 스택 개발',
                description_en='Developed low-power firmware and BLE stack for battery-powered sensor nodes',
                start_date=date(2018, 3, 1), end_date=date(2021, 2, 28),
            ),
            dict(
                category='education', order=3,
                title_ko='전자공학 학사, OO대학교', title_en='B.S. in Electronic Engineering',
                description_ko='졸업 프로젝트: Cortex-M 기반 소형 로봇 제어 보드 설계',
                description_en='Capstone project: Cortex-M based control board for a small robot',
                start_date=date(2014, 3, 1), end_date=date(2018, 2, 28),
            ),
        ]
        for data in timeline_data:
            TimelineEntry.objects.get_or_create(title_ko=data['title_ko'], defaults=data)
        self.stdout.write(self.style.SUCCESS('Timeline entries ensured'))

        skill_data = {
            ('언어', 'Languages'): ['C', 'C++', 'Python'],
            ('RTOS', 'RTOS'): ['FreeRTOS', 'Zephyr'],
            ('MCU', 'MCU'): ['STM32', 'ESP32', 'AVR'],
            ('통신', 'Communication'): ['CAN', 'Modbus', 'BLE'],
        }
        for order, ((name_ko, name_en), skills) in enumerate(skill_data.items(), start=1):
            category, _ = SkillCategory.objects.get_or_create(
                name_ko=name_ko, defaults=dict(name_en=name_en, order=order)
            )
            for s_order, skill_name in enumerate(skills, start=1):
                Skill.objects.get_or_create(category=category, name=skill_name, defaults=dict(order=s_order))
        self.stdout.write(self.style.SUCCESS('Skill categories ensured'))

        project_data = [
            dict(
                slug='can-gateway', order=1,
                title_ko='산업용 CAN 게이트웨이', title_en='Industrial CAN Gateway',
                summary_ko='다중 PLC 통신 브릿지 및 실시간 모니터링 펌웨어',
                summary_en='Multi-PLC communication bridge with real-time monitoring firmware',
                overview_ko='여러 대의 PLC와 상위 시스템 사이를 중계하는 산업용 게이트웨이 펌웨어를 개발했습니다.',
                overview_en='Developed gateway firmware bridging multiple PLCs with an upstream monitoring system.',
                role_ko='펌웨어 아키텍처 설계 및 CAN/Modbus 통신 스택 구현을 담당했습니다.',
                role_en='Responsible for firmware architecture and the CAN/Modbus communication stack.',
                architecture_ko='CAN 트랜시버 → MCU → Modbus TCP 게이트웨이 순으로 데이터를 중계하는 구조입니다.',
                architecture_en='Data flows from CAN transceiver to MCU to a Modbus TCP gateway layer.',
                tech_stack='C, CAN, Modbus, FreeRTOS, STM32',
                start_date=date(2022, 1, 1), end_date=date(2023, 6, 30),
            ),
            dict(
                slug='low-power-sensor-node', order=2,
                title_ko='저전력 환경 센서 노드', title_en='Low-Power Environmental Sensor Node',
                summary_ko='3년 배터리 수명을 목표로 한 BLE 센서 디바이스',
                summary_en='BLE sensor device engineered for a 3-year battery life target',
                overview_ko='코인셀 배터리로 3년 이상 구동되는 것을 목표로 한 저전력 환경 센서 노드입니다.',
                overview_en='A low-power environmental sensor node designed to run 3+ years on a coin cell.',
                role_ko='저전력 슬립 모드 설계 및 BLE 광고 주기 최적화를 담당했습니다.',
                role_en='Designed low-power sleep modes and optimized BLE advertising intervals.',
                architecture_ko='센서 → MCU 저전력 모드 → BLE 광고 패킷 전송 주기적 구조입니다.',
                architecture_en='Sensor readings flow through MCU low-power states into periodic BLE advertisements.',
                tech_stack='C, ESP32, BLE, 저전력 설계',
                start_date=date(2019, 4, 1), end_date=date(2020, 12, 31),
            ),
            dict(
                slug='bldc-foc-controller', order=3,
                title_ko='BLDC 모터 제어 보드', title_en='BLDC Motor Control Board',
                summary_ko='FOC 알고리즘 기반 정밀 속도 제어 시스템',
                summary_en='Precision speed control system based on the FOC algorithm',
                overview_ko='FOC(Field-Oriented Control) 알고리즘을 적용한 BLDC 모터 정밀 제어 보드를 개발했습니다.',
                overview_en='Developed a BLDC motor control board applying Field-Oriented Control for precise speed regulation.',
                role_ko='제어 알고리즘 구현 및 실시간 전류 센싱 루프 튜닝을 담당했습니다.',
                role_en='Implemented the control algorithm and tuned the real-time current-sensing loop.',
                architecture_ko='전류 센서 → ADC → FOC 연산 → PWM 출력의 실시간 제어 루프입니다.',
                architecture_en='A real-time control loop from current sensor through ADC, FOC computation, to PWM output.',
                tech_stack='C, STM32, FOC, 실시간 제어',
                start_date=date(2021, 1, 1), end_date=date(2021, 9, 30),
            ),
        ]
        for data in project_data:
            Project.objects.get_or_create(slug=data['slug'], defaults=data)
        self.stdout.write(self.style.SUCCESS('Sample projects ensured'))

        self.stdout.write(self.style.SUCCESS('Demo data seeding complete.'))

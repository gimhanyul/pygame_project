import pygame
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("블랙잭")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 폰트 설정
font = pygame.font.Font(None, 36)

# 카드 덱 생성 (모양 제외)
def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']  # 11부터 A의 숫자를 나타냄
    deck = [{'rank': rank} for rank in ranks]
    random.shuffle(deck)
    return deck

# 카드 이미지 로드 함수 (숫자 이미지)
def load_card_images():
    card_images = {}
    for i in range(2, 15):  # 2부터 14까지, A를 14로 표현
        filename = f"images/{i}.png"  # 카드 이미지 파일명 예시: '2.png', '3.png', ..., '14.png'
        card_images[str(i)] = pygame.image.load(filename)
    return card_images

# 카드 이미지 그리기
def draw_cards(hand, x, y):
    for i, card in enumerate(hand):
        card_text = get_card_text(card)
        card_image = card_images[card_text]
        screen.blit(card_image, (x + i * 90, y))

# 마지막 결과 출력
def display_final_result(player_hand, dealer_hand, result_text):
    screen.fill(WHITE)
    draw_cards(player_hand, 50, 300)
    draw_cards(dealer_hand, 50, 50)
    result_surface = font.render(result_text, True, BLACK)
    screen.blit(result_surface, (50, 200))

    # 누가 이겼는지 확인
    player_total = calculate_hand(player_hand)
    dealer_total = calculate_hand(dealer_hand)
    if player_total == dealer_total:
        final_result_text = "It's a tie!"
    elif player_total > 21 or (dealer_total <= 21 and dealer_total > player_total):
        final_result_text = "Dealer wins!"
    else:
        final_result_text = "Player wins!"

    final_result_surface = font.render(final_result_text, True, RED)
    screen.blit(final_result_surface, (50, 250))

    pygame.display.flip()
    pygame.time.wait(3000)

# 게임 실행 함수
def play_blackjack():
    deck = create_deck()
    player_hand = []
    dealer_hand = []
    score = 0  # 점수 초기화
    consecutive_wins = 0  # 연속 승리 횟수 초기화


    # 처음에 두 장씩 카드 나눠주기
    for _ in range(1):
        player_hand.append(deck.pop())
        dealer_hand.append(deck.pop())

    # 게임 루프
    running = True
    while running:
        screen.fill(WHITE)

        # 플레이어와 딜러의 카드 그리기
        draw_cards(player_hand, 50, 300)
        draw_cards(dealer_hand, 50, 50)

        # 레이블 추가
        player_label = font.render("Player", True, BLACK)
        dealer_label = font.render("Dealer", True, BLACK)
        screen.blit(player_label, (50, 260))
        screen.blit(dealer_label, (50, 20))

        # 카드 합 계산
        player_total = calculate_hand(player_hand)
        dealer_total = calculate_hand(dealer_hand)

        # 결과 확인
        if player_total == 21:
            result_text = "Blackjack! You won!"
            running = False
        elif player_total > 21:
            result_text = "The total value of the cards exceeded 21. You lost"
            running = False
        else:
            result_text = "Would you like to draw another card? (Hit/Stand)"

        result_surface = font.render(result_text, True, BLACK)
        screen.blit(result_surface, (50, 200))

        pygame.display.flip()

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # 히트(Hit)
                    player_hand.append(deck.pop())
                elif event.key == pygame.K_s:  # 스탠드(Stand)
                    while dealer_total < 17:
                        dealer_hand.append(deck.pop())
                        dealer_total = calculate_hand(dealer_hand)
                    running = False

    # 마지막 결과 출력
    display_final_result(player_hand, dealer_hand, result_text)
    pygame.quit()


# 카드 값을 계산하는 함수
def calculate_hand(hand):
    total = 0
    ace_count = 0

    for card in hand:
        if card['rank'].isdigit():
            total += int(card['rank'])
        elif card['rank'] in ['11', '12', '13']:  # J, Q, K는 각각 11, 12, 13으로 표현
            total += 10
        else:  # A
            ace_count += 1
            total += 11

    # Ace 처리
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1

    return total

# 카드 이미지 로드
card_images = load_card_images()

# 카드 이미지 텍스트 반환
def get_card_text(card):
    return card['rank']

# 게임 실행
play_blackjack()

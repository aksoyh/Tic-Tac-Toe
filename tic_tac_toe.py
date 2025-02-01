import time
from collections import deque

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    # Yatay kontrol
    for row in board:
        if all(cell == player for cell in row):
            return True
            
    # Dikey kontrol
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
            
    # Çapraz kontrol
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2-i] == player for i in range(3)):
        return True
        
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def remove_oldest_move(board, moves):
    if moves:  # Eğer hamle varsa
        oldest_move = moves.popleft()  # En eski hamleyi sil
        row, col = oldest_move
        board[row][col] = " "
        return True
    return False

def get_move_with_timeout(player, player_moves):
    # Eğer oyuncunun 2 hamlesi varsa süre sayacını başlat
    if len(player_moves) >= 2:
        start_time = time.time()
    else:
        start_time = None
        
    move = int(input(f"Oyuncu {player}, lütfen bir sayı girin (1-9): ")) - 1
    
    # Süreyi sadece 2 hamle varsa kontrol et
    if start_time is not None:
        elapsed_time = time.time() - start_time
        return move, elapsed_time
    return move, 0

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = 0
    player_moves = {
        "X": deque(),
        "O": deque()
    }
    
    print("Tic-tac-toe oyununa hoş geldiniz!")
    print("Hamle yapmak için 1-9 arası bir sayı girin:")
    print("1|2|3\n4|5|6\n7|8|9")
    print("DİKKAT: İki hamleniz varken, üçüncü hamleyi 10 saniye içinde yapmazsanız en eski hamleniz silinir!")
    
    while True:
        print_board(board)
        player = players[current_player]
        
        try:
            move, elapsed_time = get_move_with_timeout(player, player_moves[player])
            row = move // 3
            col = move % 3
            
            if move < 0 or move > 8:
                print("Lütfen 1 ile 9 arasında bir sayı girin!")
                continue
                
            if board[row][col] != " ":
                print("Bu hücre dolu! Başka bir yer seçin.")
                continue
            
            # Eğer 3 hamle varsa, en eski hamleyi sil
            if len(player_moves[player]) >= 3:
                print(f"Oyuncu {player}'in maksimum hamle sayısına ulaşıldı. En eski hamle siliniyor...")
                remove_oldest_move(board, player_moves[player])
            # Süre kontrolü - sadece 2 hamle varsa ve süre aşımı olduysa
            elif len(player_moves[player]) >= 2 and elapsed_time > 10:
                print(f"Süre aşımı! Oyuncu {player}'in en eski hamlesi siliniyor...")
                remove_oldest_move(board, player_moves[player])
            
            # Yeni hamleyi ekle
            board[row][col] = player
            player_moves[player].append((row, col))
            
            if check_winner(board, player):
                print_board(board)
                print(f"Tebrikler! Oyuncu {player} kazandı!")
                break
                
            if is_board_full(board):
                print_board(board)
                print("Oyun berabere!")
                break
                
            current_player = (current_player + 1) % 2
            
        except ValueError:
            print("Geçersiz giriş! Lütfen 1 ile 9 arasında bir sayı girin.")

if __name__ == "__main__":
    main() 
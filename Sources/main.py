import numpy # Cung cấp các loại dữ liệu và hàm tính toán cho mảng đa chiều, một cấu trúc dữ liệu phổ biến trong tính toán khoa học
import os # Thư viện để thao tác với các thư mục, tập tin và thực thi các lệnh hệ thống
import pygame # Thư viện đồ họa máy tính và thư viện âm thanh được thiết kế để sử dụng với Python.
import bfs # Module thiết kế thuật toán tìm kiếm theo chiều rộng BFS
import astar # Module thiết kế thuật toán tìm đường đi trên đồ thị

# Thời gian chờ đợi cho mỗi thuật toán 5p = 300s
TIME_OUT = 300
# Trả về đường dẫn thư mục đang làm việc dưới dạng String
path_board = os.getcwd() + '\\..\\Testcases' # Đường dẫn của thư mục Testcase
path_checkpoint = os.getcwd() + '\\..\\Checkpoints' # Đường dẫn của thư mục Checkpoints

# Duyệt các file trong Testcase và trả lại tập bảng 
def get_boards():
	os.chdir(path_board) # Chọn thư mục làm việc là Testcase
	list_boards = [] # Tạo một danh sách để lưu các ma trận Testcase
	for file in os.listdir(): # Duyệt tất cả các file hoặc thư mục có trong thư mục Testcase
		if file.endswith(".txt"): # Nếu các file có đuôi .txt thì thực hiện 
			file_path = f"{path_board}\{file}" # Lưu đường dẫn của 1 file vào file_path
			board = get_board(file_path) # Từ 1 đường dẫn đến file, thực hiện đọc và lưu lại ma trận Testcase
			list_boards.append(board) # Thêm các ma trận mới vào danh sách
	return list_boards # Trả về danh sách các ma trận Testcase

# Đoc 1 file trong Testcase
def get_board(path):
    # result giúp lưu lại ma trận đã đọc được
    # Ở đây sử dụng numpy.loadtxt để đọc dữ liêu từ tệp văn bản
    # path là đường dẫn của file cần đọc dữ liệu
    # dtype là loại dữ liệu cần đọc (ở đây đọc dữ liệu str)
    # delimiter là ký tự sử dụng để phân cách các giá trị trong file
	result = numpy.loadtxt(f"{path}", dtype=str, delimiter=',')
	for row in result: # Duyệt và định dạng lại tất cả các kí tự trong ma trận đầu vào 
		format_row(row)
	return result # Trả về nội dung đã đọc của 1 file trong Checkpoint

# Định dạng lại ma trận đầu vào của	1 file trong Testcase
def format_row(row):
	for i in range(len(row)):
		if row[i] == '1': # Nếu là 1 thì chuyển thành #
			row[i] = '#'
		elif row[i] == 'p': # Nếu là p thì chuyển thành @
			row[i] = '@'
		elif row[i] == 'b': # Nếu là b thì chuyển thành $
			row[i] = '$'
		elif row[i] == 'c': # Nếu là c thì chuyển thành %
			row[i] = '%'
   
# Duyệt các file trong Checkpoints và trả lại tập các  điểm cần kiếm tra
def get_check_points():
	os.chdir(path_checkpoint) # Chọn thư mục làm việc là Checkpoints
	list_check_point = [] # Tạo danh sách để lưu lại các ma trận điểm cần kiếm tra khi test
	for file in os.listdir(): # Duyệt tất cả các file hoặc thư mục có trong thư mục Checkpoints
		if file.endswith(".txt"): # Nếu các file có đuôi .txt thì thực hiện 
			file_path = f"{path_checkpoint}\{file}" # Lưu đường dẫn của 1 file vào file_path
			check_point = get_pair(file_path) # Từ 1 đường dẫn đến file, thực hiện đọc và lưu lại ma trận Checkpoitns
			list_check_point.append(check_point) # Thêm các ma trận mới vào danh sách
	return list_check_point # Trả về danh sách ma trận Checkpoint

# Đọc 1 file trong Checkpoint
def get_pair(path):
    # result giúp lưu lại ma trận đã đọc được
    # Ở đây sử dụng numpy.loadtxt để đọc dữ liêu từ tệp văn bản
    # path là đường dẫn của file cần đọc dữ liệu
    # dtype là loại dữ liệu cần đọc (ở đây đọc dữ liệu str)
    # delimiter là ký tự sử dụng để phân cách các giá trị trong file
	result =numpy.loadtxt(f"{path}", dtype=int, delimiter=',')
	return result # Trả về nội dung đã đọc của 1 file trong Checkpoint

# Khai báo 2 biến lưu lại ma trận bản đồ và điểm cần kiếm tra
maps = get_boards()
check_points = get_check_points()

pygame.init() # Khởi tạo pygame
pygame.font.init() # Khởi tạo máy định dạng phông chữ (font) của pygame
screen = pygame.display.set_mode((640, 640)) # Tạo của sổ pygame cỡ 640x640
pygame.display.set_caption('Sokoban') # Đặt tiêu đề cho cửa sổ pygame
clock = pygame.time.Clock() # Sử dụng để giới hạn số lần khung hình được cập nhật mỗi giây để đảm bảo rằng trò chơi của bạn không chạy quá nhanh
WHITE = (255, 255, 255) # Khởi tạo biến lưu màu trắng

# Tạo các biến khởi tạo các icon của game
assets_path = os.getcwd() + "\\..\\Assets" # Trả về đường dẫn của thư mục Assets
os.chdir(assets_path) # Chọn thư mục cần làm việc là Assets
# Lấy các icon cần thiết phục vụ cho trò chơi qua các hình ảnh
player = pygame.image.load(os.getcwd() + '\\player.png') # Lấy ra icon người đẩy hộp qua ảnh
player = pygame.transform.scale(player,(32,32)) # Thay đổi kích thước của icon người đẩy hộp 32x32
wall = pygame.image.load(os.getcwd() + '\\wall.png') # Lấy ra icon tường
box = pygame.image.load(os.getcwd() + '\\box.png') # Lấy ra icon hộp
point = pygame.image.load(os.getcwd() + '\\point.png') # Lấy ra icon các điểm hộp cần di chuyển đến
space = pygame.image.load(os.getcwd() + '\\space.png') # Lấy ra icon các khoảng trống mà hộp có thể đi qua
arrow_left = pygame.image.load(os.getcwd() + '\\arrow_left.png') # Lấy ra icon mũi tên sang trái
arrow_right = pygame.image.load(os.getcwd() + '\\arrow_right.png') # Lấy ra icon mũi tên sang phải
background = pygame.image.load(os.getcwd() + '\\background.png') # Lấy ra backgroud của game

# Hiển thị ma trận của trò chơi ra màn hình
def renderMap(board):
	width = len(board[0]) # Lấy ra số hàng
	height = len(board) # Lấy ra số cột
	# Tính khoảng cách sao cho ma trận khi in ra nằm ở giữa của cửa sổ pygame
	# Mỗi ô của ma trận có kích thước 32x32. Vì vật khi nhân với số cột sẽ ra được chiều rộng của ma trận đó
	# Mà của sổ pygame ban đầu quy định là 640. khi trừ đi chiều rộng của ma trận rồi chia đôi sẽ tính được khoảng các từ mép của sổ pygame đến cột đầu tiên
	# Vì vậy ma trận cần thụt vào so với cửa sổ pygame được lưu vào indent
	indent = (640 - width * 32) / 2.0
	# Sử dụng 2 vòng for để có thể in ra màn hình ma trận bản đồ
	for i in range(height): # Số hàng
		for j in range(width): # Số cột
      		# Đầu tiên sẽ hiển thị tất cả các ô của bản đồ với tọa độ (w,h) là ảnh space (hình mà player có thể đi qua)
			# Khi in sẽ phải thụt vào bên trái indent và cách mép trên cửa sổ 250
			# Các ô đều có cỡ 32x32 vì vậy cần nhân với 32 để đảm bảo các ô ko bị nằm lên nhau
			screen.blit(space, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '#': # Nếu như ô nào đó có kí tự là # thì hiển thị hình bức tường đã cài đặt từ trước
				screen.blit(wall, (j * 32 + indent, i * 32 + 250)) # In ra với tọa độ đã giải thích ở trên
			if board[i][j] == '$': # Nếu như ô có kí tự là $ thì hiển thị hình cái thùng đã cài đặt từ trước
				screen.blit(box, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '%': # Nếu như ô có kí tự là % thì hiển thị hình hộp cần di chuyển đến đã cài đặt từ trước
				screen.blit(point, (j * 32 + indent, i * 32 + 250))
			if board[i][j] == '@': # Nếu như ô có kí tự là @ thì hiển thị hình người đẩy thùng đã cài đặt từ trước
				screen.blit(player, (j * 32 + indent, i * 32 + 250))

# Tạo biến để in ra các level theo thứ tự nếu di chuyển mũi tên của người chơi trong danh sách bản đồ
mapNumber = 0
# Chọn thuật toán để giải quyết trò chơi (Breadth First Search, A Star Search)
algorithm = "Breadth First Search" # Ở đây chọn mặc định là BFS
# Tạo biến sceneState để lưu trạng thái hoạt động
# Ban đầu đặt là init để chọn bản đồ muốn chơi
sceneState = "init"

# Hàm Sokoban
def sokoban():
	running = True # Khai bảo biến chạy game với việc chạy vô hạn (khi hết level này có thể chạy tiếp level khác)
	global sceneState # Các trạng thái hoạt động của game
	global algorithm # Lưu thuật toán sử dụng để bot thực hiện giải
	# List_board lưu lại 2 thông tin gồm: Danh sách các bước để giải quyết bài toán
	# và số lượng trạng thái đã truy cập trong quá trình tìm kiếm
	global list_board 
	global mapNumber # Lưu bản đồ muốn chọn để bot giải
	stateLenght = 0 # Khởi tạo số bước cần di chuyển
	currentState = 0 # bước thứ n hiện tại chạy từ 1 -> stateLenght
	found = False # Kiểm tra xem có tồn tại cách giải quyết bài toán hay không

	while running:
		screen.blit(background, (0, 0)) # Hiển thị ảnh backgroud đã cài đặt bên trên
		if sceneState == "init": # Ban đầu nếu chưa chọn level nào để chạy thì cần chọn bản đồ muốn chơi
			initGame(maps[mapNumber]) # Chọn một bản đồ mong muốn có trong menu
   
		if sceneState == "executing": # Nếu như trạng thái hoạt động là thực thi thì tiến hành cho bot giải trò chơi
			# Sau khi bot nhận tín hiệu thực thi nó sẽ tìm điểm cần kiểm tra tương ứng với bản đồ ở trên
			list_check_point = check_points[mapNumber]
			# Ở bước này thì bot sẽ nhận biết xem người chơi muốn nó thực hiện theo thuật toán nào
			if algorithm == "Breadth First Search": # Nếu như người chơi muốn sử dụng thuật toán BFS
				print("BFS")
				# gọi thuật toán tìm kiếm BFS từ module bfs
				list_board = bfs.BFS_search(maps[mapNumber], list_check_point)
			else: # Nếu như người chơi muốn sử dụng thuật toán A*
				print("AStar")
				# gọi thuật toán tìm đường đi trên đồ thị A* từ module astar
				list_board = astar.AStart_Search(maps[mapNumber], list_check_point)
			# Sẽ lưu lại danh sách các bước để giải quyết bài toán và số lượng trạng thái đã truy cập trong quá trình tìm kiếm vào danh sách list_board
			if len(list_board) > 0: # Nếu như có tồn tại cách giải quyết bài toán thì cho bot giải game
				sceneState = "playing" # Chuyển trạng thái game về playing
				stateLenght = len(list_board[0]) # Lấy số bước cần di chuyển để dẩy hộp đúng chỗ
				currentState = 0 # Khởi tạo biến để đếm khi in ra khi di chuyển ở các bước
			else: # Ngược lại nếu như mà không tồn tại cách giải thì cần dừng lại để chuyển qua level khác
				sceneState = "end" # Trạng thái hoạt động dừng lại
				found = False # Đánh dấu không tồn tại cách giải quyết bài toán
    
		if sceneState == "loading": # Nếu chọn xong 1 level nào đó thì bot sẽ tiến hành tìm kiếm bản đồ
			loadingGame() # Hiển thị giao diện loading (chờ đợi bot tìm kiếm bản đồ)
			sceneState = "executing" # Sau quá trình loading bot sẽ tìm thấy bản đồ với Testcase tương ướng
									 # Sau khi tìm thấy sẽ chuyển lại trạng thái hoạt động về executing (thực thi) để bot tiến hành giải
          
		if sceneState == "end": # Nếu trạng thái game đã dùng lại thì tiến hành kiểm tra
			if found: # Nếu có tồn tại cách giải quyết thì hiển thị kết quả cuối cùng
				foundGame(list_board[0][stateLenght - 1]) # Hiển thị kết quả cuối cùng của việc di chuyển
			else: # Ngược lại nếu như không tồn tại cách giải quyết thì hiển thị ra không thế giải game
				notfoundGame() # In ra không thế giải game
		if sceneState == "playing": # Trạng thái hoạt động là playing
			clock.tick(2) # Tốc độ khung hình của trò chơi
			renderMap(list_board[0][currentState]) # In ra toàn bộ bản đồ sau mỗi lần di chuyển
			currentState = currentState + 1 # Mỗi lần di chuyển sẽ tăng biến lên 1 để có thể cập nhật lên màn hình đủ các bước nó di chuyển
			if currentState == stateLenght: # Nếu như đã in ra đủ hết các lượt di chuyển
				sceneState = "end" # Chuyển trạng thái về dừng lại để in ra kết quả cuối cùng của việc di chuyển
				found = True # Khi mà bot có thể playing thì chứng tỏ nó có thế giải game vì vậy biến found càn để là True để hiển thị ra kết quả cuối cùng
    
		# Kiểm tra các sự kiện khi nhấn vào bàn phím
		for event in pygame.event.get(): # Vòng for giúp lấy hết các sự kiện của pygame
			if event.type == pygame.QUIT: # Nếu như sự kiện pygame.QUIT thì tiến hành dùng việc chơi game và đóng cửa sổ pygame
				running = False # Ở đây đặt running=False để kết thúc vòng lặp while ở trên và thoát khỏi trò chơi bằng pygame.quit() ở cuối vòng lặp
    
			# Kiểm tra sự kiện người dùng nhấn một phím trên bàn phím
			if event.type == pygame.KEYDOWN:
				# Nhấn phím mũi tên sang trái hoặc phải để thay đổi level bản đồ
				if event.key == pygame.K_RIGHT and sceneState == "init": # Nếu như đang ở trạng thái ban đầu và người dùng bấm mũi tên sang phải
					if mapNumber < len(maps) - 1: # Nếu như level ko phải là level cuối thì có thể bấm sang phải
						mapNumber = mapNumber + 1 # Tăng level nên 1
				if event.key == pygame.K_LEFT and sceneState == "init": # Nếu như đang ở trạng thái ban đầu và người dùng bấm mũi tên sang trái
					if mapNumber > 0: # Nếu như level đó ko phải level đầu thì có thể bấm sang trái
						mapNumber = mapNumber - 1 # Giảm level xuống 1
      
				# Nhấn phím ENTER để thực hiện chọn level bản đồ và thuật toán để giải quyết bài toán
				if event.key == pygame.K_RETURN: # Kiểm tra sự kiện nhấn phím ENTER của người dùng
					if sceneState == "init": # Nếu như đang ở trạng thái ban đầu thì chuyển sang trạng thái loading để bot tìm kiếm bản đồ
						sceneState = "loading"
					if sceneState == "end": # Sau mỗi lần bot giải xong người chơi có thể nhấn ENTER để chọn level khác cho bot giải
						sceneState = "init"
				# Nhấn phím SPACE để chuyển đổi thuật toán tìm kiếm nếu muốn
				if event.key == pygame.K_SPACE and sceneState == "init": # Nếu như đang ở trạng thái ban đầu và người dùng bấm phím SPACE
					if algorithm == "Breadth First Search": # Với mỗi lần bấm nếu là thuật toán BFS thì cần chuyển về A*
						algorithm = "A Star Search"
					else: # Ngược lại nếu như đang ở thuật toán A* thì cần chuyển lại về BFS
						algorithm = "Breadth First Search"
		pygame.display.flip() # Sau khi bắt được các sự kiện cần cập nhật lại cửa sổ pygame 
	pygame.quit() # Nếu như sự kiện running=False thì sử dụng hàm này thoát khỏi chương trình pygame

# Các cảnh màn hình
# Cảnh màn hình ban đầu của trò chơi
def initGame(map):
	titleSize = pygame.font.Font('gameFont.ttf', 60) # Tạo đối tượng font với font chữ chỉ định trong file game.Font.ttf và cỡ chữ là 60
	titleText = titleSize.render('Sokoban', True, WHITE) # Tạo 1 đối tượng chứa kí tự cần hiển thị ra với màu trắng theo quy định, True là in đậm chữ
	titleRect = titleText.get_rect(center=(320, 80)) # Tạo hình chữ nhật chứa chữ Sohodan với tâm của hình chữ nhật có tọa độ (320,80)
	screen.blit(titleText, titleRect) # Hiển thị chữ lên màn hình với tọa độ đã quy định

	desSize = pygame.font.Font('gameFont.ttf', 20) # Giả thích tương tự như trên
	desText = desSize.render('Now, select your map!!!', True, WHITE)
	desRect = desText.get_rect(center=(320, 140))
	screen.blit(desText, desRect)

	mapSize = pygame.font.Font('gameFont.ttf', 30) # Giải thích tương tự như trên 
	mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
	mapRect = mapText.get_rect(center=(320, 200))
	screen.blit(mapText, mapRect)

	screen.blit(arrow_left, (246, 188)) # In ra mũi tên sang trái với tọa độ (246,188)
	screen.blit(arrow_right, (370, 188)) # In ra mũi tên sang phải với tọa độ (370,188)

	algorithmSize = pygame.font.Font('gameFont.ttf', 30) # Giải thích tương tự như trên
	algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
	algorithmRect = algorithmText.get_rect(center=(320, 600))
	screen.blit(algorithmText, algorithmRect)
	renderMap(map) # In ra ma trận bản đồ của từng Testcase được chọn

# Cảnh loading của trò chơi
def loadingGame():
	screen.blit(background, (0, 0)) # Hiển thị background đã cài đặt từ trước

	fontLoading_1 = pygame.font.Font('gameFont.ttf', 40) # Giải thích tương tự như trên
	text_1 = fontLoading_1.render('SHHHHHHH!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 300))
	screen.blit(text_1, text_rect_1)

	fontLoading_2 = pygame.font.Font('gameFont.ttf', 20) # Giải thích tương tự như trên 
	text_2 = fontLoading_2.render('The problem is being solved, stay right there!', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 340))
	screen.blit(text_2, text_rect_2)

# Cảnh hiển thị kết quả đã giải xong game
def foundGame(map):
	screen.blit(background, (0, 0)) # Hiển thị background đã cài đặt từ trước

	font_1 = pygame.font.Font('gameFont.ttf', 30) # Giải thích tương tự như trên 
	text_1 = font_1.render('Yeah! The problem is solved!!!', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 100))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 20) # Giải thích tương tự như trên 
	text_2 = font_2.render('Press Enter to continue.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 600))
	screen.blit(text_2, text_rect_2)

	renderMap(map) # In ra ma trận bản đồ của từng Testcase được chọn

# Cảnh không tìm thấy cách giải quyết bài toán
def notfoundGame():
	screen.blit(background, (0, 0)) # Hiển thị background đã cài đặt từ trước

	font_1 = pygame.font.Font('gameFont.ttf', 40) # Giải thích tương tự như trên 
	text_1 = font_1.render('Oh no, I tried my best :(', True, WHITE)
	text_rect_1 = text_1.get_rect(center=(320, 100))
	screen.blit(text_1, text_rect_1)

	font_2 = pygame.font.Font('gameFont.ttf', 20) # Giải thích tương tự như trên 
	text_2 = font_2.render('Press Enter to continue.', True, WHITE)
	text_rect_2 = text_2.get_rect(center=(320, 600))
	screen.blit(text_2, text_rect_2)

# Gọi hàm Sokoban để người dùng cho bot chơi game
sokoban()


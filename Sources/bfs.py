import support_function as spf  # Import module support_function như một đối tượng spf, và module time.
import time
def BFS_search(board, list_check_point):
    start_time = time.time()  # Gán giá trị cho biến start_time là thời điểm bắt đầu thực hiện thuật toán.
    if spf.check_win(board, list_check_point):  # Kiểm tra xem bảng ban đầu có phải là kết quả hay không, hoặc có bất kỳ điểm kiểm tra nào hay không.
        print("Found win")
        return [board]  # Nếu đúng thì trả về board ban đầu.
    start_state = spf.state(board, None, list_check_point)  # khởi tạo trạng thái ban đầu
    list_state = [start_state]  # khơi tạo 2 danh sách dùng để tìm kiếm BFS
    list_visit = [start_state]
    while len(list_visit) != 0:  # lặp qua danh sách đã truy cập
        now_state = list_visit.pop(0)  # Lặp qua danh sách list_visit đến khi nó trống. Lấy trạng thái hiện tại now_state để tìm kiếm. Tìm vị trí hiện tại của người chơi cur_pos. Nếu cần, in ra màn hình để hiển thị quá trình hoạt động của thuật toán.
        cur_pos = spf.find_position_player(now_state.board)  # nhận vị trí hiện tại của người chơi
        list_can_move = spf.get_next_pos(now_state.board,cur_pos)  # lấy danh sách vị trí mà người chơi có thể di chuyển đến
        for next_pos in list_can_move:  # tạo các trạng thái mà người chơi có thể di chuyển tới và lưu vào danh sách
            new_board = spf.move(now_state.board, next_pos, cur_pos, list_check_point)
            if spf.is_board_exist(new_board, list_state):  # nếu board chưa có trong danh sách trước thì skip the state
                continue
            if spf.is_board_can_not_win(new_board,list_check_point):  # nếu một hoặc nhiều hộp bị vứt vào góc thì skip the state
                continue
            if spf.is_all_boxes_stuck(new_board, list_check_point):  # nếu tất cả hộp đều mắc kẹt thì skip the state
                continue
            new_state = spf.state(new_board, now_state,list_check_point)  # Tạo trạng thái mới new_state. Nếu trạng thái mới là kết quả, trả về nó và số lượng trạng thái đã duyệt qua.
            if spf.check_win(new_board, list_check_point):
                print("Found win")
                return (new_state.get_line(), len(list_state))
            list_state.append(new_state)  # thêm trạng thái mới vào danh sách đã truy cập và danh sách đã qua
            list_visit.append(new_state)
            end_time = time.time()
            if end_time - start_time > spf.TIME_OUT:  # Nếu quá thời gian giới hạn, trả về danh sách rỗng.
                return []
        end_time = time.time()
        if end_time - start_time > spf.TIME_OUT:  # Nếu quá thời gian giới hạn, trả về danh sách rỗng.
            return []
    print("Not Found")  # không tìm được giải pháp
    return []
package com.example.carrot_backend.user.controller;


import com.example.carrot_backend.common.dto.ApiResponse;
import com.example.carrot_backend.user.application.UserService;
import com.example.carrot_backend.user.controller.dto.MyPageResponseDto;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/mypage")
    public ResponseEntity<ApiResponse<MyPageResponseDto>> getMyPage(HttpServletRequest request) {

        HttpSession session = request.getSession(false);
        var email = (String)session.getAttribute("USER_EMAIL");

        log.info("email: {}", email);

        var response = userService.getMyPage(email);



        log.info("response data = {}, {}, {}", response.getNickname(), response.getProfileUrl(), email);

        return ResponseEntity.ok(ApiResponse.success("마이페이지 조회 성공",  response));
    }
}

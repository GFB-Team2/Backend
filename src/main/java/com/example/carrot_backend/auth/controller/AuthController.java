package com.example.carrot_backend.auth.controller;


import com.example.carrot_backend.auth.application.AuthService;
import com.example.carrot_backend.auth.domain.LoginRequest;
import com.example.carrot_backend.common.dto.ApiResponse;
import com.example.carrot_backend.user.domain.UserEntity;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginResponseDto>> login(
            @RequestBody LoginRequestDto loginRequest,
            HttpServletRequest httpRequest
    ){
        var response = authService.login(loginRequest);

        HttpSession session = httpRequest.getSession();

        session.setAttribute("USER_EMAIL", response.getEmail());
        session.setMaxInactiveInterval(3600);

        return ResponseEntity.ok(ApiResponse.success("로그인 성공", response));
    }

    @PostMapping("/signup")
    public ResponseEntity<ApiResponse<String>> signup(
            @RequestBody @Valid SignUpRequestDto signUpRequestDto
    ){
        authService.signUp(signUpRequestDto);
        return ResponseEntity.ok(ApiResponse.success("회원가입 성공", signUpRequestDto.getEmail()));
    }


}

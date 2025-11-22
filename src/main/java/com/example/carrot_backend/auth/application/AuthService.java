package com.example.carrot_backend.auth.application;

import com.example.carrot_backend.auth.controller.LoginRequestDto;
import com.example.carrot_backend.auth.controller.LoginResponseDto;
import com.example.carrot_backend.auth.controller.SignUpRequestDto;
import com.example.carrot_backend.user.domain.UserEntity;
import com.example.carrot_backend.user.domain.UserReader;
import com.example.carrot_backend.user.domain.UserWriter;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {

    private final UserReader userReader;
    private final UserWriter userWriter;

    public LoginResponseDto login(LoginRequestDto loginRequest) {

        UserEntity user = userReader.findByEmail(loginRequest.getEmail())
                .orElseThrow(() -> new RuntimeException("아이디 또는 비밀번호가 일치하지 않습니다."));

        if (!user.getPassword().equals(loginRequest.getPassword())) {
            throw new RuntimeException("아이디 또는 비밀번호가 일치하지 않습니다.");
        }

        return LoginResponseDto.builder()
                .email(user.getEmail())
                .password(user.getPassword())
                .name(user.getName())
                .build();
    }

    @Transactional
    public void signUp(SignUpRequestDto SignUpRequest) {

        if (userReader.existsByEmail(SignUpRequest.getEmail())) {
            throw new RuntimeException("이미 존재하는 이메일입니다.");
        }

        UserEntity user = UserEntity.builder()
                            .name(SignUpRequest.getName())
                            .email(SignUpRequest.getEmail())
                            .password(SignUpRequest.getPassword())
                            .nickname(SignUpRequest.getNickname())
                            .build();

        userWriter.save(user);

    }

}

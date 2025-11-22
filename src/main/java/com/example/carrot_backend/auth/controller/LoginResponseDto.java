package com.example.carrot_backend.auth.controller;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotNull;
import lombok.*;

@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class LoginResponseDto {

    @NotNull
    @Email
    private String email;

    @NotNull
    private String password;

    @NotNull
    private String name;

}

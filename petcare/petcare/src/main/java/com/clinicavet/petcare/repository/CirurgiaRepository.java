package com.clinicavet.petcare.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.clinicavet.petcare.model.Cirurgia;

public interface CirurgiaRepository extends JpaRepository<Cirurgia, Long> {
    
} 
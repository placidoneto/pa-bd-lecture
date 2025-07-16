package com.clinicavet.petcare.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.clinicavet.petcare.model.Medicamento;

public interface MedicamentoRepository extends JpaRepository<Medicamento, Long> {

}
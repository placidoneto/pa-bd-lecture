package com.tpquarkus.resource;

import java.util.List;

import com.tpquarkus.DTO.AlunoDTO;
import com.tpquarkus.service.AlunoService;

import jakarta.inject.Inject;
import jakarta.validation.Valid;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;


@Path("/alunos")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AlunoResource {

    @Inject
    AlunoService service;

    @GET
    public List<AlunoDTO> list() {
        return service.listarTodos();
    }

    @GET
    @Path("/{id}")
    public AlunoDTO get(@PathParam("id") Long id) {
        return service.buscarPorId(id);
    }

    @POST
    public Response create(@Valid AlunoDTO dto) {
        AlunoDTO criado = service.criar(dto);
        return Response.status(Response.Status.CREATED).entity(criado).build();
    }

    @GET
    @Path("/ativo")
    public List<AlunoDTO> listActive() {
        return service.listarAtivos();
    }

    @GET
    @Path("/desativados")
    public List<AlunoDTO> listInactive() {
        return service.listarDesativados();
    }

    @PUT
    @Path("/{id}")
    public AlunoDTO update(@PathParam("id") Long id, @Valid AlunoDTO dto) {
        return service.atualizar(id, dto);
    }
}

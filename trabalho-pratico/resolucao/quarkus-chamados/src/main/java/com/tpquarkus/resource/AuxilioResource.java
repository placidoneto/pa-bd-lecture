package com.tpquarkus.resource;

import java.util.List;


import com.tpquarkus.DTO.AuxilioDTO;
import com.tpquarkus.service.AuxilioService;
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

@Path("/auxilios")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AuxilioResource {

    @Inject
    AuxilioService service;

    @GET
    public List<AuxilioDTO> list() {
        return service.listarTodos();
    }

    @GET
    @Path("/{id}")
    public AuxilioDTO get(@PathParam("id") Long id) {
        return service.buscarPorId(id);
    }

    @POST
    public Response create(@Valid AuxilioDTO dto) {
        AuxilioDTO criado = service.criar(dto);
        return Response.status(Response.Status.CREATED).entity(criado).build();
    }

    @GET
    @Path("/ativo")
    public List<AuxilioDTO> listActive() {
        return service.listarAtivos();
    }

    @GET
    @Path("/desativados")
    public List<AuxilioDTO> listInactive() {
        return service.listarDesativados();
    }

    @PUT
    @Path("/{id}")
    public AuxilioDTO update(@PathParam("id") Long id, @Valid AuxilioDTO dto) {
        return service.atualizar(id, dto);
    }
}
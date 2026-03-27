import pytest
from api.utils import calculate_distance, get_client_coordinates
from unittest.mock import patch, AsyncMock, MagicMock

def test_calculate_distance():
    # Miraflores to Barranco (roughly)
    miraflores = (-12.1223, -77.0298)
    barranco = (-12.1487, -77.0211)
    
    distance = calculate_distance(miraflores, barranco)
    
    # Distance should be around 3km
    assert 2.5 < distance < 3.5

@pytest.mark.asyncio
async def test_get_client_coordinates_local():
    coords = await get_client_coordinates("127.0.0.1")
    assert coords == (-12.1223, -77.0298)

@pytest.mark.asyncio
async def test_get_client_coordinates_remote():
    with patch("httpx.AsyncClient") as mock_client_class:
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "status": "success",
            "lat": -12.0464,
            "lon": -77.0428
        }
        mock_client.get.return_value = mock_response
        
        # Test with an IP (will be anonymized to .0)
        coords = await get_client_coordinates("190.235.154.12")
        
        assert coords == (-12.0464, -77.0428)
        # Verify that it called with .0
        mock_client.get.assert_called_with("http://ip-api.com/json/190.235.154.0?fields=status,lat,lon")
